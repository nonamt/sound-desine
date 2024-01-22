# sound-desine
**SD-DR1:** A sine wave generator (Co-developer)

Development: 12/2022 - 

Language: Python

The program generates sinusoidal sound waves based on user input. PyAudio and NumPy are used for audio processing and mathematical functionalities, respectively. Sine waves are sampled at a predetermined sampling rate: a sequence of values within the interval [-1, 1] is generated and stored in a NumPy array. The frequency and the volume of the sine wave are determined by the user; a frequency can be entered as a floating-point number or by using the twelve-tone scale. A PyAudio stream is opened according to the user input and continues processing until stopped by the user. Sound can be manipulated, for example, by adding simultaneous, new streams and by pausing, restarting, or closing existing ones.
