// Constants

const short EV_KEY = 1;
const short EV_ABS = 3;

const short BTN_CROSS = 304;
const short BTN_CIRCLE = 305;
const short BTN_SQUARE = 308;
const short BTN_TRIANGLE = 307;
const short BTN_L1 = 310;
const short BTN_L2 = 312;
const short BTN_L3 = 317;
const short BTN_R1 = 311;
const short BTN_R2 = 313;
const short BTN_R3 = 318;
const short BTN_SHARE = 314;
const short BTN_OPTIONS = 315;
const short BTN_PS = 316;

const short ABS_X = 0;
const short ABS_Y = 1;
const short ABS_Z = 2;
const short ABS_RX = 3;
const short ABS_RY = 4;
const short ABS_RZ = 5;
const short ABS_HAT0X = 16;
const short ABS_HAT0Y = 17;

/*
Evtest output for the dualshock4:

Supported events:
  Event type 0 (EV_SYN)
  Event type 1 (EV_KEY)
    Event code 304 (BTN_SOUTH)
    Event code 305 (BTN_EAST)
    Event code 307 (BTN_NORTH)
    Event code 308 (BTN_WEST)
    Event code 310 (BTN_TL)
    Event code 311 (BTN_TR)
    Event code 312 (BTN_TL2)
    Event code 313 (BTN_TR2)
    Event code 314 (BTN_SELECT)
    Event code 315 (BTN_START)
    Event code 316 (BTN_MODE)
    Event code 317 (BTN_THUMBL)
    Event code 318 (BTN_THUMBR)
  Event type 3 (EV_ABS)
    Event code 0 (ABS_X)
      Value    130
      Min        0
      Max      255
      Flat      15
    Event code 1 (ABS_Y)
      Value    126
      Min        0
      Max      255
      Flat      15
    Event code 2 (ABS_Z)
      Value      0
      Min        0
      Max      255
      Flat      15
    Event code 3 (ABS_RX)
      Value    125
      Min        0
      Max      255
      Flat      15
    Event code 4 (ABS_RY)
      Value    126
      Min        0
      Max      255
      Flat      15
    Event code 5 (ABS_RZ)
      Value      0
      Min        0
      Max      255
      Flat      15
    Event code 16 (ABS_HAT0X)
      Value      0
      Min       -1
      Max        1
    Event code 17 (ABS_HAT0Y)
      Value      0
      Min       -1
      Max        1
  Event type 4 (EV_MSC)
    Event code 4 (MSC_SCAN)
  Event type 21 (EV_FF)
    Event code 80 (FF_RUMBLE)
    Event code 81 (FF_PERIODIC)
    Event code 88 (FF_SQUARE)
    Event code 89 (FF_TRIANGLE)
    Event code 90 (FF_SINE)
    Event code 96 (FF_GAIN)
*/