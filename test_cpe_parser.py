import unittest

import cpe_parser


class TestCPEParser(unittest.TestCase):
    def test_valid_slash_red_hat(self):
        self.assertEqual(
            cpe_parser.process_cpe_str(r"cpe:2.3:o:IBM/Red_Hat:RHEL:8.4.2-1:*:*:*:*:*:*:*"),
            {
                "part": "o",
                "vendor": "IBM\/Red_Hat",
                "product": "RHEL",
                "version": "8\.4\.2\-1",
                "update": "ANY",
                "edition": "ANY",
                "language": "ANY",
                "sw_edition": "ANY",
                "target_sw": "ANY",
                "target_hw": "ANY",
                "other": "ANY",
            },
        )

    def test_valid_hyphen_mozilla(self):
        self.assertEqual(
            cpe_parser.process_cpe_str(r"cpe:2.3:a:mozilla:firefox:esr-78.16.0:*:*:*:*:*:*:*"),
            {
                "part": "a",
                "vendor": "mozilla",
                "product": "firefox",
                "version": "esr\-78\.16\.0",
                "update": "ANY",
                "edition": "ANY",
                "language": "ANY",
                "sw_edition": "ANY",
                "target_sw": "ANY",
                "target_hw": "ANY",
                "other": "ANY",
            },
        )

    def test_valid_hyphen_ios(self):
        self.assertEqual(
            cpe_parser.process_cpe_str(r"cpe:2.3:o:apple:ios:15.1-beta:*:.:*:*:*:*:-"),
            {
                "part": "o",
                "vendor": "apple",
                "product": "ios",
                "version": "15\.1\-beta",
                "update": "ANY",
                "edition": "\.",
                "language": "ANY",
                "sw_edition": "ANY",
                "target_sw": "ANY",
                "target_hw": "ANY",
                "other": "NA",
            },
        )

    def test_valid_multiple_dots_and_hyphens(self):
        self.assertEqual(
            cpe_parser.process_cpe_str(r"cpe:2.3:h:-:acrobat_reader:DC-2019.012.20051:-:-:-:.:.:.:*"),
            {
                "part": "h",
                "vendor": "NA",
                "product": "acrobat_reader",
                "version": "DC\-2019\.012\.20051",
                "update": "NA",
                "edition": "NA",
                "language": "NA",
                "sw_edition": "\.",
                "target_sw": "\.",
                "target_hw": "\.",
                "other": "ANY",
            },
        )

    def test_invalid_missing_parts(self):
        self.assertRaises(ValueError, cpe_parser.process_cpe_str, cpe_string=r"cpe:2.3:h:-:acrobat_reader:DC-2019.012.20051:-:-:-*")

    def test_invalid_asterisk_in_middle(self):
        self.assertRaises(ValueError, cpe_parser.process_cpe_str, cpe_string=r"cpe:2.3:h:-:acrob*at_reader:DC-2019.012.20051:-:-:-*")

    def test_invalid_quote_in_middle(self):
        self.assertRaises(ValueError, cpe_parser.process_cpe_str, cpe_string=r"cpe:2.3:h:-:acrob?at_reader:DC-2019.012.20051:-:-:-*")

    def test_invalid_missing_version(self):
        self.assertRaises(ValueError, cpe_parser.process_cpe_str, cpe_string=r"cpe::h:-:acrob?at_reader:DC-2019.012.20051:-:-:-*")


if __name__ == "__main__":
    unittest.main()
