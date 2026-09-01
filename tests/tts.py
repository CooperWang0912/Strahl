import genie_tts as genie

genie.load_predefined_character('thirtyseven')

genie.tts(
    character_name='thirtyseven',
    text='This is a TTS inference test',
    play=True,
)

genie.wait_for_playback_done()