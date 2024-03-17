from mqtt import *
from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from event_manager import *
from machine import Pin, SoftI2C
from aiot_dht20 import DHT20
from homebit3_lcd1602 import LCD1602
import sys
import uselect
from aiot_rgbled import RGBLed
from machine import RTC
import ntptime
import time

def on_mqtt_message_receive_callback__V10_(th_C3_B4ng_tin):
  global Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  if th_C3_B4ng_tin == '1':
    pin10.write_digital((1))
  else:
    pin10.write_digital((0))

def on_mqtt_message_receive_callback__V11_(th_C3_B4ng_tin):
  global Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  if th_C3_B4ng_tin == '1':
    pin13.write_digital((1))
  else:
    pin13.write_digital((0))

# Mô tả hàm này...
def _C4_90_C4_83ng_K_C3_AD_K_C3_AAnh_D_E1_BB_AF_Li_E1_BB_87u():
  global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM, aiot_dht20, aiot_lcd1602, tiny_rgb, lcd1602
  mqtt.on_receive_message('V10', on_mqtt_message_receive_callback__V10_)
  mqtt.on_receive_message('V11', on_mqtt_message_receive_callback__V11_)

event_manager.reset()

aiot_dht20 = DHT20(SoftI2C(scl=Pin(22), sda=Pin(21)))

lcd1602 = LCD1602()

def on_event_timer_callback_T_U_a_j_H():
  global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  aiot_dht20.read_dht20()
  RT = aiot_dht20.dht20_temperature()
  RH = aiot_dht20.dht20_humidity()
  SM = translate((pin1.read_analog()), 0, 4096, 0, 100)
  LUX = pin2.read_analog()
  aiot_lcd1602.move_to(0, 0)
  aiot_lcd1602.putstr('RT:')
  aiot_lcd1602.move_to(3, 0)
  aiot_lcd1602.putstr(RT)
  aiot_lcd1602.move_to(7, 0)
  aiot_lcd1602.putstr('*C')
  aiot_lcd1602.move_to(10, 0)
  aiot_lcd1602.putstr('RH:')
  aiot_lcd1602.move_to(13, 0)
  aiot_lcd1602.putstr(RH)
  aiot_lcd1602.move_to(15, 0)
  aiot_lcd1602.putstr('%')
  aiot_lcd1602.move_to(0, 1)
  aiot_lcd1602.putstr('LUX')
  aiot_lcd1602.move_to(4, 1)
  aiot_lcd1602.putstr('      ')
  aiot_lcd1602.move_to(4, 1)
  aiot_lcd1602.putstr(LUX)
  aiot_lcd1602.move_to(10, 1)
  aiot_lcd1602.putstr('SM:')
  aiot_lcd1602.move_to(13, 1)
  aiot_lcd1602.putstr(SM)
  aiot_lcd1602.move_to(15, 1)
  aiot_lcd1602.putstr('%')
  mqtt.publish('V1', RT)
  mqtt.publish('V2', RH)
  mqtt.publish('V3', SM)
  mqtt.publish('V4', LUX)

event_manager.add_timer_event(30000, on_event_timer_callback_T_U_a_j_H)

def read_terminal_input():
  spoll=uselect.poll()        # Set up an input polling object.
  spoll.register(sys.stdin, uselect.POLLIN)    # Register polling object.

  input = ''
  if spoll.poll(0):
    input = sys.stdin.read(1)

    while spoll.poll(0):
      input = input + sys.stdin.read(1)

  spoll.unregister(sys.stdin)
  return input

tiny_rgb = RGBLed(pin0.pin, 4)

def on_event_timer_callback_Q_W_a_A_F():
  global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  Chu_E1_BB_97i_AI = read_terminal_input()
  if len(Chu_E1_BB_97i_AI) > 0:
    L_E1_BB_87nh_AI = Chu_E1_BB_97i_AI[0]
    if L_E1_BB_87nh_AI == 'A':
      Tr_E1_BA_A1ng_Th_C3_A1i = 'BINH THUONG'
      tiny_rgb.show(0, hex_to_rgb('#00ff00'))
    if L_E1_BB_87nh_AI == 'B':
      Tr_E1_BA_A1ng_Th_C3_A1i = 'VANG LA'
      tiny_rgb.show(0, hex_to_rgb('#ffff00'))

event_manager.add_timer_event(2000, on_event_timer_callback_Q_W_a_A_F)

def on_event_timer_callback_y_h_r_l_B():
  global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  mqtt.publish('V6', Tr_E1_BA_A1ng_Th_C3_A1i)

event_manager.add_timer_event(60000, on_event_timer_callback_y_h_r_l_B)

def on_event_timer_callback_I_q_y_I_i():
  global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  if LUX >= 2000:
    GDD = (GDD if isinstance(GDD, (int, float)) else 0) + 1
    mqtt.publish('V5', GDD)
  print('{' + 'x' + ': ' + str(LUX) + '}')

event_manager.add_timer_event(60000, on_event_timer_callback_I_q_y_I_i)

def on_event_timer_callback_a_y_g_W_o():
  global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  if SM < 50:
    pin10.write_digital((1))
    mqtt.publish('V10', '1')
  if SM > 80:
    pin10.write_digital((0))
    mqtt.publish('V10', '0')

event_manager.add_timer_event(60000, on_event_timer_callback_a_y_g_W_o)

def on_event_timer_callback_A_B_p_u_j():
  global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  Th_E1_BB_9Di_Gian = (int(('%0*d' % (2, RTC().datetime()[4])))) * 60
  Th_E1_BB_9Di_Gian = (Th_E1_BB_9Di_Gian if isinstance(Th_E1_BB_9Di_Gian, (int, float)) else 0) + (int(('%0*d' % (2, RTC().datetime()[5]))))
  if Th_E1_BB_9Di_Gian > 420:
    pin13.write_digital((1))
    mqtt.publish('V11', '1')
  if Th_E1_BB_9Di_Gian > 435:
    pin13.write_digital((0))
    mqtt.publish('V11', '0')
  if Th_E1_BB_9Di_Gian > 840:
    pin13.write_digital((1))
    mqtt.publish('V11', '1')
  if Th_E1_BB_9Di_Gian > 870:
    pin13.write_digital((0))
    mqtt.publish('V11', '0')

event_manager.add_timer_event(60000, on_event_timer_callback_A_B_p_u_j)

def on_event_timer_callback_D_z_g_o_J():
  global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_Gian, RT, Tr_E1_BA_A1ng_Th_C3_A1i, GDD, RH, L_E1_BB_87nh_AI, LUX, SM
  Th_E1_BB_9Di_Gian = (int(('%0*d' % (2, RTC().datetime()[4])))) * 10
  Th_E1_BB_9Di_Gian = (Th_E1_BB_9Di_Gian if isinstance(Th_E1_BB_9Di_Gian, (int, float)) else 0) + (int(('%0*d' % (2, RTC().datetime()[5]))))
  if Th_E1_BB_9Di_Gian > 420:
    pin13.write_digital((1))
    mqtt.publish('V11', '1')
  if Th_E1_BB_9Di_Gian > 435:
    pin13.write_digital((0))
    mqtt.publish('V11', '0')
  if Th_E1_BB_9Di_Gian > 840:
    pin13.write_digital((1))
    mqtt.publish('V11', '1')
  if Th_E1_BB_9Di_Gian > 870:
    pin13.write_digital((0))
    mqtt.publish('V11', '0')

event_manager.add_timer_event(60000, on_event_timer_callback_D_z_g_o_J)

if True:
  display.scroll('SmartGreenhouse')
  mqtt.connect_wifi('abcd', '123456789')
  mqtt.connect_broker(server='io.adafruit.com', port=1883, username='dadnbk123456', password='aio_ygOP94FUl1KpXYlkjWQDNPdZvL4Z')
  display.scroll('OK')
  ntptime.settime()
  (year, month, mday, week_of_year, hour, minute, second, milisecond) = RTC().datetime()
  RTC().init((year, month, mday, week_of_year, hour+7, minute, second, milisecond))
  lcd1602.clear()
  _C4_90_C4_83ng_K_C3_AD_K_C3_AAnh_D_E1_BB_AF_Li_E1_BB_87u()
  GDD = 0

while True:
  mqtt.check_message()
  event_manager.run()
  time.sleep_ms(1000)
