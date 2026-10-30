import trezorui_api
from trezor.crypto import bip39
from trezor.ui.layouts.common import interact_simple
from trezor.ui.layouts.eckhart.recovery import request_word


async def show_bip39_last_word_candidates() -> None:
    words: list[str] = [""] * 23
    index = 0
    send_button_request = True

    while index < len(words):
        word = await request_word(
            word_index=index,
            word_count=len(words),
            is_slip39=False,
            send_button_request=send_button_request,
            prefill_word=words[index],
        )
        send_button_request = False

        if not word:
            if index == 0:
                return
            words[index] = ""
            index -= 1
            continue

        words[index] = word
        index += 1

    prefix = " ".join(words)

    try:
        candidates = bip39.last_word_candidates(prefix)
    except ValueError:
        with trezorui_api.show_simple(
            title="Invalid BIP39 prefix",
            text="Check the 23 words and try again.",
        ) as layout:
            await interact_simple(layout)
        return

    text = "\n".join(
        f"{index + 1}. {word}" for index, word in enumerate(candidates)
    )
    with trezorui_api.show_simple(
        title="BIP39 last-word candidates",
        text=text,
    ) as layout:
        await interact_simple(layout)
