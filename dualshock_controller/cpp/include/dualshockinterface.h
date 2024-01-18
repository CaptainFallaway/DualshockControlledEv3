#include <thread>
#include <mutex>
#include <fstream>

struct EventData {
    long timestamp;
    long timestamp_decimal;
    short type;
    short code;
    int value;
};

class EventDataRegistrar {
    public:
        EventDataRegistrar();
        void set(EventData& eventData);
        EventData get(bool clearRegister);
    private:
        EventData eventData;
        std::mutex mutex;
};

class DualshockInterface {
public:
    DualshockInterface(const std::string& eventStreamPath);

    ~DualshockInterface();

    EventDataRegistrar btnCross;
    EventDataRegistrar btnCircle;
    EventDataRegistrar btnSquare;
    EventDataRegistrar btnTriangle;
    EventDataRegistrar btnL1;
    EventDataRegistrar btnL2;
    EventDataRegistrar btnL3;
    EventDataRegistrar btnR1;
    EventDataRegistrar btnR2;
    EventDataRegistrar btnR3;
    EventDataRegistrar btnShare;
    EventDataRegistrar btnOptions;
    EventDataRegistrar btnPS;

    EventDataRegistrar axisLeftStickX;
    EventDataRegistrar axisLeftStickY;
    EventDataRegistrar axisRightStickX;
    EventDataRegistrar axisRightStickY;
    EventDataRegistrar axisL2;
    EventDataRegistrar axisR2;
    EventDataRegistrar axisDPadX;
    EventDataRegistrar axisDPadY;

    void startListening();

    void stop();
private:
    const std::string eventStreamPath;

    std::ifstream eventStream;

    std::thread loopThread;
    bool stopRequested;

    void loop();

    void checkEventStream();

    void handleKeyEvent(EventData& event);

    void handleAxisEvent(EventData& event);
};