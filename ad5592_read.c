#ifndef SOURCES_AD5592RPI_H_
#define SOURCES_AD5592RPI_H_

/**
 * 	Change the #include to use the Serial Peripheral Diver header.
 */
#include <bcm2835.h>

/**
 * Define the number of bytes in a standard word for the
 * SPI device used.
 */
#define SPI_WORD_BYTES				1U		/* Number of bytes in SPI word for device */

/**
 * Control register definitions.
 * Refer to page 26 of AD5592R datasheet Rev A.
 */
#define AD5592_CNTRL_ADDRESS_MASK	0x7800	/* Control register bit mask */
#define	AD5592_NOP					0x0000	/* No operation */
#define	AD5592_DAC_READBACK			0x0800	/* Selects and enables DAC read back */
#define	AD5592_ADC_READ				0x1000	/* Selects ADCs for conversion */
#define	AD5592_GP_CNTRL				0x1800	/* General purpose control register */
#define	AD5592_ADC_PIN_SELECT		0x2000	/* Selects which pins are ADC inputs */
#define AD5592_DAC_PIN_SELECT		0x2800	/* Selects which pins are DAC outputs */
#define	AD5592_PULL_DOWN_SET		0x3000	/* Selects which pins have 85kOhm pull-down resistor to GND */
#define	AD5592_CNTRL_REG_READBACK	0x3800	/* Read back control registers and/or set LDAC */
#define	AD5592_GPIO_WRITE_CONFIG	0x4000	/* Selects which pins are GPIO outputs */
#define	AD5592_GPIO_WRITE_DATA		0x4800	/* Writes data to the GPIO outputs */
#define	AD5592_GPIO_READ_CONFIG		0x5000	/* Selects which pins are GPIO inputs */
#define AD5592_GPIO_READ_INPUT		0x5400	/* Read GPIO inputs */
#define	AD5592_POWER_DWN_REF_CNTRL	0x5800	/* Powers down DACs and enables/disables the reference */
#define	AD5592_GPIO_DRAIN_CONFIG	0x6000	/* Selects open-drain or push/pull for GPIO outputs */
#define AD5592_THREE_STATE_CONFIG	0x6800	/* Selects which pins are three-state */
#define	AD5592_SW_RESET				0x7DAC	/* Software reset of the AD5592 */

/**
 * Pins
 */
#define AD5592_IO0	0x01
#define AD5592_IO1	0x02
#define AD5592_IO2	0x04
#define	AD5592_IO3	0x08
#define	AD5592_IO4	0x10
#define	AD5592_IO5	0x20
#define	AD5592_IO6	0x40
#define	AD5592_IO7	0x80

#define AD5592_PIN_SELECT_MASK		0x00FF	/* Pin select bit mask */

/**
 * DAC register definitions.
 */
#define AD5592_DAC_WRITE_MASK		0x8000	/* DAC write bit mask */
#define AD5592_DAC_ADDRESS_MASK		0x7000	/* DAC pin address bit mask */
#define AD5592_DAC_VALUE_MASK		0x0FFF	/* DAC output value bit mask */

/**
 * Other useful macros
 */
#define	SHORT_DELAY	10		/* Delay used to let device do it's thing */
#define LONG_DELAY	50		/* Longer delay to give it more time */

#define CHANNEL0			BCM2835_SPI_CS0
#define	CHANNEL1			BCM2835_SPI_CS1

char spiOut[2]; 			/* SPI output buffer */
char spiIn[2];	 			/* SPI input buffer  */

uint16_t mV;					/* millivolts */
uint16_t result;				/* result */
uint8_t digitalOutPins = 0x00;	/* Bit mask of pins currently set as digital out */
uint8_t digitalInPins = 0x00;	/* Bit mask of pins currently set as digital in */
uint8_t analogOutPins = 0x00;	/* Bit mask of pins currently set as analog out */
uint8_t analogInPins = 0x00;	/* Bit mask of pins currently set as analog in */

typedef unsigned short int	AD5592_WORD;

/**
 * Clear the spi buffer.
 * Parameters:
 * 	spiBuffer[] = spi buffer
 */
void clearBuffer(char spiBuffer[]);

/**
 * Parse the 16 bit word of the AD5592 into two 8 bit chunks that
 * works with the bcm2835 library.
 * Parameters:
 * 	eightBits[] = spi buffer
 * 	sixteenBits = AD5592 spi word
 */
void makeWord(char eightBits[], AD5592_WORD sixteenBits);

/**
 * Select the SPI channel.
 * Parameters:
 * 	ch = channel number
 */
void setAD5592Ch(int ch);

/**
 * Convert a voltage to an digital value based upon assumptions of
 * 0 - 5V input and 12 bit ADC/DAC.
 * Parameter: millivolts as 16 bit unsigned integer
 * Returns: digital value as 16 bit unsigned integer
 */
 uint16_t a2d(uint16_t millivolts);

/**
 * Convert a digital value to voltage based upon assumptions of
 * 0 - 5V input and 12 bit ADC/DAC.
 * Parameter: digital value as 16 bit unsigned integer
 * Returns: millivolts as 16 bit unsigned integer
 */
uint16_t d2a(uint16_t count);

/**
 * Set pins to digital outputs.
 * Parameter: Pins as bit mask
 */
void setAsDigitalOut(uint8_t pins);

/**
 * Set pins to a digital inputs.
 * Parameter: Pins as bit mask
 */
 void setAsDigitalIn(uint8_t pins);

/**
 * Set pins to analog outputs.
 * Parameter: Pins as bit mask
 */
void setAsDAC(uint8_t pins);

/**
 * Set pins to a analog inputs.
 * Parameter: Pins as bit mask
 */
 void setAsADC(uint8_t pins);
 
 void setAsPULLDOWN(uint8_t pins);

/**
 * SPI communications
 * Parameter:
 * 	Command to send.
 */
void spiComs(AD5592_WORD command);

/**
 * Set a pin to high or low output.
 * Parameters:
 * 	Pins to output as bit mask
 * 	State to be output as bit mask
 */
void setDigitalOut(uint8_t pins, uint8_t states);
void setDigitalOut(uint8_t pins, uint8_t states);

/**
 * Get the digital input states
 * Parameter:
 * 	Pins to read as digital inputs as bit mask
 * Returns:
 * 	Pin states as bit mask. Unused pins are 0s.
 */
uint8_t getDigitalIn(uint8_t pins);

/**
 * Set an analog output value
 * Parameters:
 * 	Pin number to write to as number (0 to 7)
 *  Value to write in milivolts (assumes 5V reference)
 */
void setAnalogOut(uint8_t pin, uint16_t milivolts);

/**
 * Get analog input value
 * Parameters:
 * 	Pin number to to get value for as number (0 to 7)
 * Returns:
 * 	milivolts (assumes 5V reference)
 */
uint16_t getAnalogIn(uint8_t pins);

long int elapsed_time();

/**
 * Initialize the SPI for using the AD5592. Does not set channel. Do that
 * after calling this function by calling setAD5592Ch().
 * Parameters:
 * 	none
 */
void AD5592_Init();

#endif /* SOURCES_AD5592RPI_H_ */

/* Main Program */

#include <stdio.h>
#include <sys/time.h>
#include <time.h>
#include <string.h>



#define ACTIVE_CHANNELS 3

int main(){
	int duration;
	printf("Setup.....\n");
	printf("Read ADC program initiated...\n\n");
	printf("------------------\n\n");
	printf("Enter sample duration (s):");
	scanf("%d", &duration);
	
	AD5592_Init();
	setAD5592Ch(0);
	spiComs(AD5592_SW_RESET);
	bcm2835_delay(100);
	//spiComs(0x1820);	//ADC gain 0-2Vref
	//bcm2835_delay(1);
	spiComs(0x20FF); //Set all pins as ADC
	analogInPins = 0xFF;
	bcm2835_delay(1);
	spiComs(0x5A00);	//Enable Internal reference
	bcm2835_delay(1);
	
	//spiComs(0x1B20);	//ADC Buffer enabled, Precharge enabled, ADC gain 0-2Vref
	//spiComs(0x1900);	//ADC Buffer enabled
	//spiComs(0x1A00);	//Precharge enabled
	//spiComs(0x1A20);	//Precharge enabled, ADC gain 0-2Vref
	spiComs(0x1AA0);	//Precharge enabled, ADC gain 0-2Vref, Lock
	
	bcm2835_delay(LONG_DELAY);
	
	uint16_t data[8] = {0};
	uint16_t result = 0;
	uint8_t index;
	int us = 0;
	FILE *filePointer;
	time_t timeStamp;
	time(&timeStamp);
	filePointer = fopen(ctime(&timeStamp), "w");
	fprintf(filePointer, "Time [us], Signal 0 [mV], Signal 1 [mV], Signal 2 [mV], Signal 3 [mV], Signal 4 [mV], Signal 5 [mV], Signal 6 [mV], Signal 7 [mV]\n");
	
	delay(5);
	
	printf("\n------------------\n\n");
	printf("Taking readings.....\n");
	gettimeofday(&st, NULL);
	
	do{
		for(int i = 0; i < ACTIVE_CHANNELS; i++){
			result = getAnalogIn(i);
			printf("Result: %u; ", result);
			data[i] = result;
			bcm2835_delay(.001);
		}
		gettimeofday(&et, NULL);
		fprintf(filePointer, "%d", elapsed_time());
		for(int j = 0; j < ACTIVE_CHANNELS; j ++){
			fprintf(filePointer, ",%u", data[j]);
		}
		fprintf(filePointer, "\n");
	}while(elapsed_time() < (duration*1000000));
	//spiComs(AD5592_ADC_READ | 0x0000);	//Multichannel stop read
	//spiComs(AD5592_NOP);
	printf("\n------------------\n\n");
	printf("Data recorded, check logs\n");
	fclose(filePointer);
	return 0;
}

struct timeval st, et;
 

long int elapsed_time(){
	long int elapsed = ((et.tv_sec - st.tv_sec) * 1000000) + (et.tv_usec - st.tv_usec);
	return elapsed;
}



/**
 * Clear the spi buffer.
 * Parameters:
 * 	spiBuffer[] = spi buffer
 */
void clearBuffer(char spiBuffer[])
{
	int i;
	for(i=0;i<strlen(spiBuffer);i++)
	{
		spiBuffer[i] = 0x00;
	}
}

/**
 * Parse the 16 bit word of the AD5592 into two 8 bit chunks that
 * works with the bcm2835 library.
 * Parameters:
 * 	eightBits[] = spi buffer
 * 	sixteenBits = AD5592 spi word
 */
void makeWord(char eightBits[], AD5592_WORD sixteenBits)
{
	clearBuffer(eightBits);
	eightBits[0] = (sixteenBits & 0xFF00) >> 8;
	eightBits[1] = sixteenBits & 0xFF;
}

/**
 * Select the SPI channel.
 * Parameters:
 * 	ch = channel number
 */
void setAD5592Ch(int ch)
{
	switch(ch){
		case 0:
			bcm2835_spi_chipSelect(CHANNEL0);
			bcm2835_spi_setChipSelectPolarity(CHANNEL0, LOW);
			break;
		case 1:
			bcm2835_spi_chipSelect(CHANNEL1);
			bcm2835_spi_setChipSelectPolarity(CHANNEL1, LOW);
			break;
	}
}

/**
 * Convert a voltage to an digital value based upon assumptions of
 * 0 - 5V input and 12 bit ADC/DAC.
 * Parameter: millivolts as 16 bit unsigned integer
 * Returns: digital value as 16 bit unsigned integer
 */
 uint16_t a2d(uint16_t millivolts)
 {
	 uint16_t count = millivolts * .819f;
	 return count;
 }

/**
 * Convert a digital value to voltage based upon assumptions of
 * 0 - 5V input and 12 bit ADC/DAC.
 * Parameter: digital value as 16 bit unsigned integer
 * Returns: millivolts as 16 bit unsigned integer
 */
uint16_t d2a(uint16_t count)
{
	uint16_t millivolts = count / .819f;
	return millivolts;
}

/**
 * Set pins to digital outputs.
 * Parameter: Pins as bit mask
 */
void setAsDigitalOut(uint8_t pins)
{
	digitalOutPins = pins;	/* Log which pins are configured */
	makeWord(spiOut, AD5592_GPIO_WRITE_CONFIG | pins); 	/* Make the word */
	bcm2835_spi_transfern(spiOut, sizeof(spiOut));		/* Send it */
}

/**
 * Set pins to a digital inputs.
 * Parameter: Pins as bit mask
 */
 void setAsDigitalIn(uint8_t pins)
{
	digitalInPins = pins;	/* Log which pins are configured */
	makeWord(spiOut, AD5592_GPIO_READ_CONFIG | pins); 	/* Make the word */
	bcm2835_spi_transfern(spiOut, sizeof(spiOut));		/* Send it */
}

/**
 * Set pins to analog outputs.
 * Parameter: Pins as bit mask
 */
void setAsDAC(uint8_t pins)
{
	analogOutPins = pins;	/* Log which pins are configured */
	makeWord(spiOut, AD5592_DAC_PIN_SELECT | pins); 	/* Make the word */
	bcm2835_spi_transfern(spiOut, sizeof(spiOut));		/* Send it */
	bcm2835_delay(SHORT_DELAY);
}

/**
 * Set pins to a analog inputs.
 * Parameter: Pins as bit mask
 */
 void setAsADC(uint8_t pins)
{
	analogInPins = pins;	/* Log which pins are configured */
	makeWord(spiOut, AD5592_ADC_PIN_SELECT | pins);		/* Make the word */
	bcm2835_spi_transfern(spiOut, sizeof(spiOut));		/* Send it */
	bcm2835_delay(SHORT_DELAY);
}

 void setAsPULLDOWN(uint8_t pins)
{
	//pullDownPins = pins;	/* Log which pins are configured */
	makeWord(spiOut, AD5592_PULL_DOWN_SET | pins);		/* Make the word */
	bcm2835_spi_transfern(spiOut, sizeof(spiOut));		/* Send it */
	bcm2835_delay(SHORT_DELAY);
}

/**
 * SPI communications
 * Parameter:
 * 	Command to send.
 */
void spiComs(AD5592_WORD command)
{
	makeWord(spiOut, command);
	clearBuffer(spiIn);
	bcm2835_spi_transfernb(spiOut, spiIn, sizeof(spiOut));
}

/**
 * Set a pin to high or low output.
 * Paramters:
 * 	All pins with a digital output as bit mask
 * 	State to be output to all diguital out pins as bit mask
 */
void setDigitalOut(uint8_t pins, uint8_t states)
{
	if(!(pins == digitalOutPins))
	{
		setAsDigitalOut(pins | digitalOutPins);
	}
	spiComs(AD5592_GPIO_WRITE_DATA | states);
}

/**
 * Get the digital input states
 * Parameter:
 * 	All pins to be configured as digital inputs as bit mask
 * Returns:
 * 	Pin states as bit mask. Unused pins are 0s.
 */
uint8_t getDigitalIn(uint8_t pins)
{
	if(!(pins == digitalInPins))
	{
		setAsDigitalIn(pins | digitalInPins);
	}
	spiComs(AD5592_GPIO_READ_INPUT | pins);
	spiComs(AD5592_NOP);

	return spiIn[1];
}

/**
 * Set an analog output value
 * Parameters:
 * 	Pin number to write to as number (0 to 7)
 *  Value to write in milivolts (assumes 5V reference)
 */
void setAnalogOut(uint8_t pin, uint16_t milivolts)
{
	if(!((analogOutPins >> pin ) & 0x1))
	{
		setAsDAC(analogOutPins | (0x1 << pin));
	}
	spiComs(AD5592_DAC_WRITE_MASK | 		/* DAC write command */
	((pin <<12) & AD5592_DAC_ADDRESS_MASK)|	/* Set which pin to write */
	a2d(milivolts));						/* Load digital value */
}

/**
 * Get analog input value
 * Parameters:
 * 	Pin number to to get value for as number (0 to 7)
 * Returns:
 * 	milivolts (assumes 5V reference)
 */
uint16_t getAnalogIn(uint8_t pin)
{
	if(!((analogInPins >> pin ) & 0x1))
	{
		setAsADC(analogInPins | (0x1 << pin));
	}
	spiComs(AD5592_ADC_READ | (0x1 << pin));
	spiComs(AD5592_NOP);
	spiComs(AD5592_NOP);
	
	uint16_t result = ((spiIn[0] << 8) & 0x0F00) | (spiIn[1] & 0xFF);
	/* Return result */
	return d2a(result);
}

/**
 * Initialize the SPI for using the AD5592. Does not set channel. Do that
 * after calling this function by calling setAD5592Ch().
 * Parameters:
 * 	none
 */
void AD5592_Init()
{
	//int msg;
	/* Initialize the bcm2835 library */
	bcm2835_init();

    /* Initialize the SPI module */
    bcm2835_spi_begin();

    /* Set SPI bit order */
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);      // The default

    /* Set SPI polarity and phase */
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE1);                   // Mode 1

    /* Set SPI clock */
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_1024); 	  // 16 = 64ns = 15.625MHz
}
 
