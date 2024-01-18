#include "constants.h"
#include "dualshockinterface.h"

#include <iostream>


EventDataRegistrar::EventDataRegistrar() : eventData(), mutex() {}

void EventDataRegistrar::set(EventData& eventData) {
    std::lock_guard<std::mutex> lock(mutex);
    this->eventData = eventData;
}

EventData EventDataRegistrar::get(bool clearRegister) {
    std::lock_guard<std::mutex> lock(mutex);
    // Copy the eventData
    EventData eventDataCopy = eventData;

    if (clearRegister) {
        eventData = EventData();
    }

    return eventDataCopy;
}


DualshockInterface::DualshockInterface(const std::string& eventStreamPath) : eventStreamPath(eventStreamPath), stopRequested(false) {};

DualshockInterface::~DualshockInterface() {
    stop();
}

void DualshockInterface::startListening() {
    loopThread = std::thread(&DualshockInterface::loop, this);
}

void DualshockInterface::stop() {
    stopRequested = true;
    eventStream.close();

    if (loopThread.joinable()) {
        loopThread.join();
    }
}

void DualshockInterface::loop() {
    // The loop that runs in a separate thread

    eventStream.open(eventStreamPath, std::ios::in | std::ios::binary);

    if (!eventStream.is_open() || eventStream.fail()) {
        throw std::runtime_error("Event stream failed to open!\nSee if controller has disconnected or changed event stream path.");
        return;
    }

    // Initialize a EventData so it can be mutated in the loop
    EventData event;

    while (!stopRequested) {
        if (eventStream.fail()) {
            throw std::runtime_error("Event stream failed to read!\nSee if controller has disconnected or changed event stream path.");
            return;
        }

        eventStream.read(reinterpret_cast<char*>(&event), sizeof(EventData));

        switch (event.type) {
            case (EV_KEY):
                handleKeyEvent(event);
                break;
            case (EV_ABS):
                handleAxisEvent(event);
                break;
            default:
                break;
        }
    }
}

void DualshockInterface::handleKeyEvent(EventData& event) {
    switch (event.code) {
        case (BTN_CROSS):
            btnCross.set(event);
            break;
        case (BTN_CIRCLE):
            btnCircle.set(event);
            break;
        case (BTN_TRIANGLE):
            btnTriangle.set(event);
            break;
        case (BTN_SQUARE):
            btnSquare.set(event);
            break;
        case (BTN_L1):
            btnL1.set(event);
            break;
        case (BTN_R1):
            btnR1.set(event);
            break;
        case (BTN_L2):
            btnL2.set(event);
            break;
        case (BTN_R2):
            btnR2.set(event);
            break;
        case (BTN_SHARE):
            btnShare.set(event);
            break;
        case (BTN_OPTIONS):
            btnOptions.set(event);
            break;
        case (BTN_PS):
            btnPS.set(event);
            break;
        case (BTN_L3):
            btnL3.set(event);
            break;
        case (BTN_R3):
            btnR3.set(event);
            break;
        default:
            break;
    }
}

void DualshockInterface::handleAxisEvent(EventData& event) {
    switch (event.code) {
        case (ABS_X):
            axisLeftStickX.set(event);
            break;
        case (ABS_Y):
            axisLeftStickY.set(event);
            break;
        case (ABS_Z):
            axisL2.set(event);
            break;
        case (ABS_RX):
            axisRightStickX.set(event);
            break;
        case (ABS_RY):
            axisRightStickY.set(event);
            break;
        case (ABS_RZ):
            axisR2.set(event);
            break;
        case (ABS_HAT0X):
            axisDPadX.set(event);
            break;
        case (ABS_HAT0Y):
            axisDPadY.set(event);
            break;
        default:
            break;
    }
}


// C interface for the DualshockInterface class to be used in Python with ctypes
extern "C" {
    DualshockInterface* DualshockInterface_new(const char* eventStreamPath) {
        return new DualshockInterface(eventStreamPath);
    }

    void DualshockInterface_delete(DualshockInterface* dualshockInterface) {
        delete dualshockInterface;
    }

    void DualshockInterface_startListening(DualshockInterface* dualshockInterface) {
        dualshockInterface->startListening();
    }

    void DualshockInterface_stop(DualshockInterface* dualshockInterface) {
        dualshockInterface->stop();
    }

    EventData DualshockInterface_getBtnCross(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnCross.get(clearRegister);
    }

    EventData DualshockInterface_getBtnCircle(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnCircle.get(clearRegister);
    }

    EventData DualshockInterface_getBtnSquare(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnSquare.get(clearRegister);
    }

    EventData DualshockInterface_getBtnTriangle(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnTriangle.get(clearRegister);
    }

    EventData DualshockInterface_getBtnL1(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnL1.get(clearRegister);
    }

    EventData DualshockInterface_getBtnL2(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnL2.get(clearRegister);
    }

    EventData DualshockInterface_getBtnL3(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnL3.get(clearRegister);
    }

    EventData DualshockInterface_getBtnR1(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnR1.get(clearRegister);
    }

    EventData DualshockInterface_getBtnR2(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnR2.get(clearRegister);
    }

    EventData DualshockInterface_getBtnR3(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnR3.get(clearRegister);
    }

    EventData DualshockInterface_getBtnShare(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnShare.get(clearRegister);
    }

    EventData DualshockInterface_getBtnOptions(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnOptions.get(clearRegister);
    }

    EventData DualshockInterface_getBtnPS(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->btnPS.get(clearRegister);
    }

    EventData DualshockInterface_getAxisLeftStickX(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->axisLeftStickX.get(clearRegister);
    }

    EventData DualshockInterface_getAxisLeftStickY(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->axisLeftStickY.get(clearRegister);
    }

    EventData DualshockInterface_getAxisRightStickX(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->axisRightStickX.get(clearRegister);
    }

    EventData DualshockInterface_getAxisRightStickY(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->axisRightStickY.get(clearRegister);
    }

    EventData DualshockInterface_getAxisL2(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->axisL2.get(clearRegister);
    }

    EventData DualshockInterface_getAxisR2(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->axisR2.get(clearRegister);
    }

    EventData DualshockInterface_getAxisDPadX(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->axisDPadX.get(clearRegister);
    }

    EventData DualshockInterface_getAxisDPadY(DualshockInterface* dualshockInterface, bool clearRegister) {
        return dualshockInterface->axisDPadY.get(clearRegister);
    }
}