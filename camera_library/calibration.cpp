#include <iostream>

class Calibration{
    public:
        void myCalibration(){
            std::cout << "Here calibration goes." << std::endl;
        }
};

int main()
{
    Calibration t; 
    t.myCalibration();  
    return 0;
}

extern "C" {
    Calibration* Calibration_new(){ return new Calibration(); }
    void Calibration_myCalibration(Calibration* calibration){ 
        calibration -> myCalibration(); 
    }
}