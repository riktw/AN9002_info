
class AN9002:
    OVERLOAD = -2
    SEGMENTERROR = -1
    
    def SetMeasuredValue(self, data):
        self.data = data
        self.overloadFlag = False
        
    def GetDisplayedValue(self):
        segment0raw = self.__GetRaw7Segment(self.data[3], self.data[4])
        segment07s = self._InvertNeeded7SegmentBits(segment0raw, 0b0100010)
        dataToDisplay = self.__Convert7SegmentToDecimal(segment07s) * 1000
        
        segment1raw = self.__GetRaw7Segment(self.data[4], self.data[5])
        segment17s = self._InvertNeeded7SegmentBits(segment1raw, 0b1010001)
        dataToDisplay += self.__Convert7SegmentToDecimal(segment17s) * 100

        segment2raw = self.__GetRaw7Segment(self.data[5], self.data[6])
        segment27s = self._InvertNeeded7SegmentBits(segment2raw, 0b1100010)
        dataToDisplay += self.__Convert7SegmentToDecimal(segment27s) * 10
        
        segment3raw = self.__GetRaw7Segment(self.data[6], self.data[7])
        segment37s = self._InvertNeeded7SegmentBits(segment3raw, 0b0010001)
        dataToDisplay += self.__Convert7SegmentToDecimal(segment37s)
        
        dataToDisplay /= self.__GetDivisionFactor()
        if not self.__CheckBit(self.data[3], 4):
            dataToDisplay *= -1.0
      
        return dataToDisplay
            
        
    def GetDisplayedUnit(self):
        if self.__CheckBit(self.data[3], 3):
            return "V (diode tester)" 
        
        if not self.__CheckBit(self.data[7], 5):
            return "F"
        elif not self.__CheckBit(self.data[7], 6):
            return "C"
        
        if self.__CheckBit(self.data[8], 4):
            if not self.__CheckBit(self.data[8], 5):
                return "mF"
            elif not self.__CheckBit(self.data[8], 6):
                return "uF"
            elif self.__CheckBit(self.data[8], 7):
                return "nF"
        
        if self.__CheckBit(self.data[9], 4):
            if not self.__CheckBit(self.data[9], 5):
                return "mV"
            else:
                return "V"
        elif not self.__CheckBit(self.data[9], 7):
            if not self.__CheckBit(self.data[10], 3):
                return "mA"
            elif self.__CheckBit(self.data[10], 2):
                return "uA"
            else:
                return "A"
                
        elif not self.__CheckBit(self.data[9], 1):
            if not self.__CheckBit(self.data[9], 3):
                return "MΩ"
            elif self.__CheckBit(self.data[9], 2):
                return "kΩ"
            else:
                return "Ω"
        elif self.__CheckBit(self.data[9], 0):
            return "Hz"
        
        return "?"

    def __CheckBit(self, byte, bitPosition):
        return True if byte & (1<<bitPosition) else False

    def __GetDivisionFactor(self):
        if self.__CheckBit(self.data[4], 4):
            return 1000.0
        elif self.__CheckBit(self.data[5], 4):
            return 100.0
        elif not self.__CheckBit(self.data[6], 4):
            return 10.0
        else:
            return 1.0
        

    def __GetRaw7Segment(self, byte1, byte2):
        high, low = byte1 & 0xE0, byte2 & 0x0F
        return ((high >> 1) + low)

    def _InvertNeeded7SegmentBits(self, segmentRaw, invertTable):
        invertedValue = segmentRaw ^ invertTable
        shuffledValue = (invertedValue & 0x40) >> 6
        shuffledValue += (invertedValue & 0x20) 
        shuffledValue += (invertedValue & 0x10) 
        shuffledValue += (invertedValue & 0x08) >> 2
        shuffledValue += (invertedValue & 0x04) << 4
        shuffledValue += (invertedValue & 0x02) << 1
        shuffledValue += (invertedValue & 0x01) << 3
        return shuffledValue

    def __Convert7SegmentToDecimal(self, raw7seg):
        if raw7seg == 0x3F:
            return 0
        elif raw7seg == 0x06:
            return 1
        elif raw7seg == 0x5B:
            return 2
        elif raw7seg == 0x4F:
            return 3
        elif raw7seg == 0x66:
            return 4
        elif raw7seg == 0x6D:
            return 5
        elif raw7seg == 0x7D:
            return 6
        elif raw7seg == 0x07:
            return 7
        elif raw7seg == 0x7F:
            return 8
        elif raw7seg == 0x6F:
            return 9
        elif raw7seg == 0x38: #L from OL, OverLoad
            self.overloadFlag = True
            return self.OVERLOAD
        else: 
            return self.SEGMENTERROR