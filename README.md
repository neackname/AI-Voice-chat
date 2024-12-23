# communication with AI by voice chat
This idea is from my another project that is led by my teacher.My first concept is create a GUI to make it more convenient
for  users to use AI.<br />

The requirements of this project :
1.TTS(Text To Speech) and STT(Speech To Text) from the Azure <br />
2.the model of vicuna. I get this model from the hugging face and its name is lmsys/vicuna-7b-v1.5<br />
3.the model of llama.cpp . from https://github.com/ggerganov/llama.cpp .We need this to accelerate vicuna to generate reply because the vicuna is so slow.Although I accelerate
it , it still slow.But i do not have any methods to slove it.But is still brought some benefits that is make the vicuna smaller.<br />
4.QT to create GUI or find java Spring boot to make web


At third commit ,you need to open the llama.cpp server on your work environment and then it can run the code
At this, we can commit a .wav on the input_wav , then use the code to create AI .wav on the output_wav


