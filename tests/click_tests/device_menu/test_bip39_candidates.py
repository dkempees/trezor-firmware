import re

import pytest

from ..recovery import enter_word
from .common import open_device_menu

pytestmark = [pytest.mark.models("eckhart")]


@pytest.mark.setup_client(pin=None)
def test_bip39_last_word_candidates(device_handler):
    debug = device_handler.debuglink()

    assert device_handler.features().initialized is True

    open_device_menu(debug)
    menu = debug.read_layout().vertical_menu_content()
    assert "BIP39 candidates" in menu

    debug.button_actions.navigate_to_menu_item(menu.index("BIP39 candidates"))

    # Enter the first word, then go back from the empty second word.
    enter_word(debug, "abandon", is_slip39=False)
    assert "MnemonicKeyboard" in debug.read_layout().all_components()
    debug.click(debug.screen_buttons.mnemonic_erase())

    # The previous word should be shown again and can be confirmed.
    assert "MnemonicKeyboard" in debug.read_layout().all_components()
    debug.click(debug.screen_buttons.mnemonic_confirm())

    for _ in range(22):
        enter_word(debug, "abandon", is_slip39=False)

    debug.synchronize_at("TextScreen")
    layout = debug.read_layout()
    assert layout.title() == "BIP39 last-word candidates"

    results = layout.text_content()
    for _ in range(layout.page_count() - 1):
        debug.click(debug.screen_buttons.ok())
        results += " " + debug.read_layout().text_content()

    candidates = re.findall(r"\b[1-8]\.\s+([a-z]+)\b", results)
    assert len(candidates) == 8, results
    assert len(set(candidates)) == 8, candidates
    assert "art" in candidates
