(() => {
  const type = document.querySelector('#lookup-type');
  const methods = [...document.querySelectorAll('input[name="lookup-method"]')];
  function updateLookup() {
    const vehicular = type.value === 'vehicular';
    document.querySelector('#lookup-plate-option').hidden = !vehicular;
    if (!vehicular) methods.find(method => method.value === 'cedula').checked = true;
    const plate = vehicular && methods.some(method => method.value === 'placa' && method.checked);
    document.querySelector('#lookup-cedula-field').hidden = plate;
    document.querySelector('#lookup-plate-field').hidden = !plate;
  }
  type.addEventListener('change', updateLookup);
  methods.forEach(method => method.addEventListener('change', updateLookup));
  updateLookup();
  // Only filter the public directory. No case identifiers are read or sent.
})();
