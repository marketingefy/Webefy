"""Read-only onboarding checks. Observed server keys are NOT trusted automatically."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from deploy_sftp import key_agent

HOST = "162.241.61.73"  # Public IP supplied in the user's HostGator server information.


def check_server():
    found = False
    with tempfile.TemporaryDirectory(prefix="efy-server-check-") as temporary:
        for port in (2222, 22):
            try:
                result = subprocess.run(
                    ["ssh-keyscan", "-4", "-T", "8", "-p", str(port),
                     "-t", "ed25519,rsa,ecdsa", HOST],
                    capture_output=True, text=True, timeout=30,
                )
            except subprocess.TimeoutExpired:
                print(f"Puerto {port}: sin respuesta dentro del tiempo de la prueba.")
                continue
            lines = sorted(set(
                line for line in result.stdout.splitlines()
                if len(line.split()) == 3 and not line.startswith("#")
            ))
            if not lines:
                print(f"Puerto {port}: no se obtuvo una clave de servidor SSH.")
                continue
            found = True
            public_file = Path(temporary) / f"server-{port}.pub"
            public_file.write_text("\n".join(lines) + "\n")
            fingerprints = subprocess.run(
                ["ssh-keygen", "-lf", str(public_file), "-E", "sha256"],
                check=True, capture_output=True, text=True,
            ).stdout
            print(f"Puerto {port}: responde SSH. Huellas observadas, pendientes de verificar:")
            print(fingerprints.strip())
            print("Entradas públicas observadas para comparar con HostGator:")
            print("\n".join(lines))
    if not found:
        print("La prueba no pudo alcanzar SSH. Esto no confirma que el servicio esté deshabilitado.")


def check_key():
    key = os.environ.get("SSH_PRIVATE_KEY", "").strip()
    if not key:
        raise ValueError("Falta SSH_PRIVATE_KEY en GitHub Secrets.")
    print("SSH_PRIVATE_KEY: presente; su contenido no se imprime.")
    with tempfile.TemporaryDirectory(prefix="efy-key-check-") as temporary:
        root = Path(temporary)
        private = root / "key"
        private.write_text(key + "\n")
        private.chmod(0o600)
        with key_agent(root, private, os.environ.get("SSH_KEY_PASSPHRASE", "")):
            print("Clave privada y contraseña: desbloqueo correcto. Sin inicio de sesión ni publicación.")


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["server"]:
            check_server()
        elif sys.argv[1:] == ["key"]:
            check_key()
        else:
            raise ValueError("Use server or key.")
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except (subprocess.SubprocessError, OSError):
        print("La comprobación no pudo completarse; revisar las herramientas y los datos configurados.", file=sys.stderr)
        sys.exit(1)
