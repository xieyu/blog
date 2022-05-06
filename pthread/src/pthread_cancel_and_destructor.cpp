#include<unistd.h>
#include<pthread.h>
#include<stdio.h>
#include<string>

pthread_t t1, t2;
pthread_key_t tlsKey;

class FakeLock {
public:
    FakeLock(const char* label);
    ~FakeLock();

private:
    std::string m_label;
};

FakeLock::FakeLock(const char* label): m_label(label){
    printf("%s constructor of  FakeLock\n", m_label.c_str());
}

FakeLock::~FakeLock() {
    printf("%s descturctor of FakeLock\n", m_label.c_str());
}

void t1_cleanup(void* args){
    printf("t1 clean up\n");
    sleep(20);
}

void* t1_run(void* args){
    printf("t1: begin\n");
    FakeLock fakelock("t1");
    pthread_cleanup_push(t1_cleanup, nullptr);
    sleep(2);
    pthread_cleanup_pop(0);
    printf("t1: end\n");
    return NULL;
}

void* t2_run(void* args) {
    printf("t2: begin\n");
    FakeLock lock("t2");
    pthread_cancel(t1);
    pthread_exit(NULL);
    printf("t2: end\n");
    return NULL;
}

int main() {
    pthread_create(&t1, NULL, t1_run, NULL);
    pthread_create(&t2, NULL, t2_run, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    //pthread_key_delete(tlsKey);
    return 0;
}
