# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 14:14:04 2022

@author: lab

Programmer's Refrence Manual:
https://www.thorlabs.com/drawings/b383388a86f3d153-2876887D-A231-167F-97FA549E02806CE4/ITC4005QCL-ProgrammersReferenceManual.pdf

USB Communication:
https://github.com/ryantro/Mode-Locked-Oscillator-Data-Logging/blob/master/USBDevice.py
"""

import pyvisa

def main():
    
    # USB ADDRESS FOR THORLABS ITC4005
    usbaddr = "USB::4883::32842::M00466376"
    
    currentCommand = "SOURce:CURRent 2.8"
    
    # ASKERS
    c1 = "SOURce:CURRent?"
    cMax = "SOURce:CURRent? MAXimum"
    c3 = "SYST:BEEP"
    
    c4 = "READ?"
    
    state = ":OUTPut?"
    on = ":OUTPut ON"
    off = ":OUTPut:STATe OFF"
    
    # SET COMMANDS
    routBNC = "INPut:ROUT BNC"
    setPulsed = "SOURce:FUNCtion:SHAPe PULSE"
    setCW = "SOURce:FUNCtion:SHAPe DC"
    
    # SET DUTY CYCLE
    dutyCycle = "10.0"
    setDutyCycle = "SOURce:PULSe:DCYCle {}".format(dutyCycle)
    
    
    # CHECKING TEST COMMANDS
    interlockTest = "OUTPut:PROTection:INTLock:TRIPped?"
    keyTest = "OUTPut:PROTection:KEYLock:TRIPped?"
    tempTest = "OUTPut:PROTection:OTEMp:TRIPped?"
    polTest = "INPut:POLarity?"
    routTest = "INPut:ROUTe?"
    currentModeTest = "SOURce:FUNCtion:MODE?"
    modeTest = "SOURce:FUNCtion:SHAPe?"
    dutyCycleTest = "SOURce:PULSe:DCYCle?"
    periodTest = "SOURce:PULse:PERiod?"
    
    periodSet = "SOURce:PULse:PERiod 0.01"
    #cMaxSet = 
    
    
    vQ = "OUTPut:PROTection:VOLTage:TRIPped?"
    eQ = "OUTPut:PROTection:EXTernal:TRIPped?"
    wQ = "OUTPut:PROTection:INTernal:TRIPped?"
    iQ = "OUTPut:PROTection:INTLock:TRIPped?"
    kQ = "OUTPut:PROTection:KEYLock:TRIPped?"
    tQ = "OUTPut:PROTection:OTEMp:TRIPped?"
    
    lst = [vQ, eQ, wQ, iQ, kQ, tQ]
    
    try:
        itc = USBDevice(usbaddr)
        print(itc.send("*IDN?"))
        
        print("Keytest (On = 0; Off = 1):")
        print(itc.send(keyTest))
        
        print("Interlock Test (Closed = 0; Open = 1):")
        print(itc.send(interlockTest))
        
        print("Temperature Test (Okay = 0; Too Hot = 1):")
        print(itc.send(tempTest))
        
        print("Polarity Test (Normal = CG; Inverted = AG):")
        print(itc.send(polTest))
        
        print("Terminal Routing Test:")
        print(itc.send(routTest))
        
        print("Pulsed or CW?:")
        print(itc.send(modeTest))
        
        print("Set duty cycle:")
        print(itc.write(setDutyCycle))
        
        print("Duty cycle?:")
        print(itc.send(dutyCycleTest))
        
        itc.write(periodSet)
        
        print("Period test?:")
        print(itc.send(periodTest))
        
        
        print("Current Max (A)?")
        print(itc.send(cMax))
        
        for Q in lst:
            response = itc.send(Q)
            if(response == "1"):
                print("Command:\n"+Q+"\nreturned a positive value.")
        
    finally:
        itc.close()
    
    return


class USBDevice:
    def __init__(self,rname):
        self.inst = pyvisa.ResourceManager().open_resource(rname)
        return None
    
    def settimeout(self,timeout):
        self.inst.timeout = timeout+1000
    
    def write(self,command):
        self.inst.write(command)
        return 0
    
    def send(self,command):
        return self.inst.query(command).strip('\r\n')
    
    def close(self):
        self.inst.close()
        return None




if __name__ == "__main__":
    main()