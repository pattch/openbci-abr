# openbci-abr
An OpenBCI Plugin that allows you to play tones and record EEG data in order to record Auditory Brainstem Responses

# Usage

Use with the OpenBCI Python's user.py script, found here: https://github.com/OpenBCI/OpenBCI_Python.
Simply drop the contents of the plugins folder into the plugins folder there and from the root directory of the OpenBCI Python repo run this command:

    python user.py --add tone
    
The user.py script should then register the tone script here and make a connection to the OpenBCI board you're using.
Finally, once everything's loaded, run the command:

    /start tone
    
And tones should automatically be played while eeg data is recorded.
