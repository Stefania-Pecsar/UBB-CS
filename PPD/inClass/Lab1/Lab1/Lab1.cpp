#include <iostream>
#include <thread>

void worker() {
    std::cout << "Hello thread!" << std::endl;
}

int main()
{
    std::thread t(worker);
    std::cout << "Hello World!\n";
    t.join();
    std::cout << "Joined thread!" << std::endl;
    return 0;
}

