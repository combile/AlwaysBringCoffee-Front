import speech_recognition as sr
from AltinoLite import*
import time as t

r =  sr.Recognizer()
null = ''

Open()
with sr.Microphone() as source:
    while 1:
        Go(300,300)
        print('상황발령')
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ko-KR')
            if text=="과속" :
                Go(600,600)

                print('1차')
                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio, language='ko-KR')
                    print("입력받은 말 : ", text)
                    if text=="도와줘" or text=="살려줘" :
                        Led(15)
                        sound(37)
                        print('비상상황인가요?')
                        audio = r.listen(source)
                        try:
                            text = r.recognize_google(audio, language='ko-KR')
                            print("입력받은 말 : ", text)
                            if ("아니" or "취소") in text:
                                Go(600,600)
                                delay(1000)
                                Go(0,0)
                                Steering(0)
                                Close()
                            break
                        except:
                            sound(61)
                            Delay(100)
                            sound(58)
                            Delay(100)
                            Go(500,500)
                            delay(500)

                            sound(61)
                            Delay(100)
                            sound(58)
                            Delay(100)
                            Go(400,400)
                            delay(500)

                            sound(61)
                            Delay(100)
                            sound(58)
                            Delay(100)
                            Go(300,300)
                            delay(500)

                            sound(61)
                            Delay(100)
                            sound(58)
                            Delay(100)
                            Go(200,200)
                            delay(500)

                            sound(61)
                            Delay(100)
                            sound(58)
                            Delay(100)
                            Go(100,100)
                            delay(500)

                            sound(61)
                            Delay(100)
                            sound(58)
                            Delay(100)
                            Sound(0)
                            Go(0,0)
                            Steering(0)
                            Close()
                            break
                except:
                    break
        except :
                continue
        
        



# 시작 300 > 과속 음성 인식시 600 > 살려줘/도와줘 인식 > 1차 비상등 (사용자한테 확인멘트)소리 > 2차 (주변 차량 비상 클락션)소리, 신고 or 상황종료


