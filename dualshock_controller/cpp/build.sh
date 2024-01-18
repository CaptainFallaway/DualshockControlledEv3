# Nothing fancy since i'm just doing a quick build on a ev3dev robot.
echo "Building libdualshockinterface.so"
g++ -Wall -shared -fPIC -Iinclude -O3 -flto -o ./build/libdualshockinterface.so ./src/dualshockinterface.cpp