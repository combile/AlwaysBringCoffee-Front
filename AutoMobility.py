import speech_recognition as sr
from AltinoLite import*
r =  sr.Recognizer()
Open()
with sr.Microphone() as source:
    print('말해 보세요 : ')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='ko-KR')
        print('음성인식 결과는 : {}'.format(text))
        if text=="자율 주행" or text=="자율주행":
            while 1 :
                try :
                    Led(15);delay(500)
                    Led(0);delay(500)
                except :
                    break
        Go(0,0)
        Steering(0)
        Close()
    except:
        print('목소리를 인식하지 못했습니다.')
