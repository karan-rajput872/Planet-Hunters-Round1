"""
Unit tests for Dashboard UI Rendering & Component Markup Integrity.
Verifies that HTML components render properly without CommonMark codeblock escaping.
"""

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from dashboard.styles import render_html
from dashboard.components.hero import render_hero
from dashboard.components.performance import render_performance
from dashboard.components.architecture import render_architecture
from dashboard.components.features import render_features
from dashboard.components.validator import render_validator
from dashboard.components.explorer import render_explorer
from dashboard.components.info import render_info

class TestDashboardRendering(unittest.TestCase):
    """Verifies dashboard components render cleanly without raw HTML leaks."""

    def test_render_html_helper_calls_st_html_when_available(self):
        """Checks that render_html prefers st.html to bypass markdown parsing."""
        with patch.object(st, "html", create=True) as mock_html, \
             patch.object(st, "markdown") as mock_markdown:
            sample_html = """
            <div class="ph-card">
                <h1>Test</h1>
            </div>
            """
            render_html(sample_html)
            mock_html.assert_called_once()
            mock_markdown.assert_not_called()
            rendered_arg = mock_html.call_args[0][0]
            self.assertTrue(rendered_arg.startswith("<div class=\"ph-card\">"))
            self.assertFalse(rendered_arg.startswith("    "))

    def test_render_html_helper_falls_back_to_markdown_cleanly(self):
        """Checks that when st.html is absent, fallback dedents cleanly."""
        original_hasattr = hasattr
        def mock_hasattr(obj, name):
            if obj is st and name == "html":
                return False
            return original_hasattr(obj, name)

        with patch("builtins.hasattr", side_effect=mock_hasattr), \
             patch.object(st, "markdown") as mock_markdown:
            sample_html = """
            <div class="ph-card">
                <h1>Test Fallback</h1>
            </div>
            """
            render_html(sample_html)
            mock_markdown.assert_called_once()
            rendered_arg = mock_markdown.call_args[0][0]
            self.assertTrue(rendered_arg.startswith("<div class=\"ph-card\">"))
            self.assertTrue(mock_markdown.call_args[1].get("unsafe_allow_html"))

    def test_render_hero_executes_without_error(self):
        """Verifies render_hero executes cleanly and passes valid markup."""
        recorded_html = []
        with patch("dashboard.components.hero.render_html", side_effect=lambda s: recorded_html.append(s)):
            render_hero("creamy")
            self.assertEqual(len(recorded_html), 1)
            content = recorded_html[0]
            # Verify Project Title & Subtitle presence
            self.assertIn("Planet Hunters", content)
            self.assertIn("Find New Worlds in Starlight", content)
            self.assertIn("Project Overview &amp; Problem Formulation", content)
            # Verify no raw HTML comments that trip markdown blocks
            self.assertNotIn("<!--", content)
            # Verify class names and styling
            self.assertIn("ph-card ph-card-accent", content)
            self.assertIn("badge-status", content)

    def test_all_components_render_cleanly(self):
        """Checks that major components execute without raising exceptions."""
        def mock_cols(spec, *args, **kwargs):
            count = spec if isinstance(spec, int) else len(spec)
            return [MagicMock() for _ in range(count)]

        def mock_selectbox(label, options, index=0, **kwargs):
            if options and len(options) > index:
                return options[index]
            return options[0] if options else None

        with patch("streamlit.markdown"), \
             patch("streamlit.html", create=True), \
             patch("streamlit.columns", side_effect=mock_cols), \
             patch("streamlit.plotly_chart"), \
             patch("streamlit.image"), \
             patch("streamlit.selectbox", side_effect=mock_selectbox), \
             patch("streamlit.text_input", return_value=""), \
             patch("streamlit.button", return_value=False), \
             patch("streamlit.download_button"):
            try:
                render_performance("creamy")
                render_architecture("creamy")
                render_features("creamy")
                render_validator("creamy")
                render_explorer("creamy")
                render_info("creamy")
            except Exception as e:
                self.fail(f"Component rendering raised exception: {e}")

    def test_render_html_strips_leading_spaces_and_blank_lines(self):
        """Checks that render_html completely strips leading whitespace from every line."""
        original_hasattr = hasattr
        def mock_hasattr(obj, name):
            if obj is st and name == "html":
                return False
            return original_hasattr(obj, name)

        with patch("builtins.hasattr", side_effect=mock_hasattr), \
             patch.object(st, "markdown") as mock_markdown:
            nested_html = """
            <div>
                <!-- comment here -->
                <p>Paragraph with leading indent</p>

                <span>Second child</span>
            </div>
            """
            render_html(nested_html)
            mock_markdown.assert_called_once()
            output = mock_markdown.call_args[0][0]
            for line in output.splitlines():
                self.assertFalse(line.startswith(" "), f"Line should not have leading spaces: {line}")
                self.assertFalse(line.startswith("\t"), f"Line should not have leading tabs: {line}")
                self.assertTrue(len(line) > 0, "Should not contain empty lines")
            self.assertNotIn("<!--", output)

    def test_validator_generates_valid_table_markup_without_indentation(self):
        """Verifies validator renders real HTML tables with zero indented lines."""
        recorded_html = []
        def mock_cols(spec, *args, **kwargs):
            count = spec if isinstance(spec, int) else len(spec)
            return [MagicMock() for _ in range(count)]

        with patch("streamlit.html", create=True, side_effect=lambda s: recorded_html.append(s)), \
             patch("streamlit.markdown", side_effect=lambda s, **kw: recorded_html.append(s)), \
             patch("streamlit.columns", side_effect=mock_cols), \
             patch("streamlit.button", return_value=False), \
             patch("streamlit.download_button"):
            render_validator("creamy")

            # Check that table HTML was passed
            table_snippets = [h for h in recorded_html if "<table" in h]
            self.assertTrue(len(table_snippets) >= 1, "Expected audit table HTML")
            total_tables = sum(h.count("<table") for h in table_snippets)
            self.assertTrue(total_tables >= 2, "Expected at least 2 audit tables (Stage A and Stage B)")

            for table_html in table_snippets:
                self.assertIn("</table>", table_html)
                self.assertIn("<tbody>", table_html)
                self.assertIn("</tbody>", table_html)
                self.assertIn("<tr", table_html)
                self.assertIn("<td", table_html)
                self.assertNotIn("<!--", table_html)
                # Verify that no lines in the table have >= 4 leading spaces
                for line in table_html.splitlines():
                    self.assertFalse(line.startswith("    "), f"Indented line detected that could trigger codeblock: {line}")

if __name__ == "__main__":
    unittest.main()

