"""The deployment cache block must preserve the hosting owner's Apache rules."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('deploy_sftp', Path(__file__).resolve().parents[1] / 'scripts/deploy_sftp.py')
deploy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deploy)


class HtmlCacheRules(unittest.TestCase):
    def test_preserves_hosting_rules_and_is_idempotent(self):
        before = '# cPanel settings\nRewriteEngine On\nRewriteRule ^secure$ /login [L]'
        merged = deploy.merge_html_cache_rules(before)
        self.assertTrue(merged.startswith(before + '\n'))
        self.assertEqual(merged.count(deploy.CACHE_START), 1)
        self.assertEqual(deploy.merge_html_cache_rules(merged), merged)

    def test_replaces_only_the_managed_block(self):
        before = 'RewriteEngine On\n'
        after = '\n# PHP handler\nAddHandler application/x-httpd-php83 .php\n'
        existing = before + deploy.CACHE_START + '\nold rules\n' + deploy.CACHE_END + after
        self.assertEqual(deploy.merge_html_cache_rules(existing), before + deploy.CACHE_RULES + after)

    def test_supports_absent_config(self):
        self.assertEqual(deploy.merge_html_cache_rules(''), deploy.CACHE_RULES + '\n')

    def test_refuses_ambiguous_blocks(self):
        for existing in [deploy.CACHE_START, deploy.CACHE_END, deploy.CACHE_END + deploy.CACHE_START, deploy.CACHE_RULES * 2]:
            with self.assertRaises(ValueError): deploy.merge_html_cache_rules(existing)


if __name__ == '__main__':
    unittest.main()
