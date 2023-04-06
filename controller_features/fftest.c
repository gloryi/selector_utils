#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <linux/input.h>

#include "bitmaskros.h"


#define N_EFFECTS 6

char* effect_names[] = {
	"Sine vibration",
	"Constant Force",
	"Spring Condition",
	"Damping Condition",
	"Strong Rumble",
	"Weak Rumble"
};

int main(int argc, char** argv)
{
	struct ff_effect effects[N_EFFECTS];
	struct input_event play, stop, gain;
	int fd;
	const char * device_file_name = "/dev/input/event0";
	unsigned char relFeatures[1 + REL_MAX/8/sizeof(unsigned char)];
	unsigned char absFeatures[1 + ABS_MAX/8/sizeof(unsigned char)];
	unsigned char ffFeatures[1 + FF_MAX/8/sizeof(unsigned char)];
	int n_effects;	/* Number of effects the device can play at the same time */
	int i;

	device_file_name = argv[1];

	/* Open device */
	fd = open(device_file_name, O_RDWR);
	if (fd == -1) {
		perror("Open device file");
		exit(1);
	}


	/* Absolute axes */
	memset(absFeatures, 0, sizeof(absFeatures)*sizeof(unsigned char));
	if (ioctl(fd, EVIOCGBIT(EV_ABS, sizeof(absFeatures)*sizeof(unsigned char)), absFeatures) == -1) {
		perror("Ioctl absolute axes features query");
		exit(1);
	}

	/* Relative axes */
	memset(relFeatures, 0, sizeof(relFeatures)*sizeof(unsigned char));
	if (ioctl(fd, EVIOCGBIT(EV_REL, sizeof(relFeatures)*sizeof(unsigned char)), relFeatures) == -1) {
		perror("Ioctl relative axes features query");
		exit(1);
	}


	memset(ffFeatures, 0, sizeof(ffFeatures)*sizeof(unsigned char));
	if (ioctl(fd, EVIOCGBIT(EV_FF, sizeof(ffFeatures)*sizeof(unsigned char)), ffFeatures) == -1) {
		perror("Ioctl force feedback features query");
		exit(1);
	}



	if (ioctl(fd, EVIOCGEFFECTS, &n_effects) == -1) {
		perror("Ioctl number of effects");
	}

	/* Set master gain to 75% if supported */
	if (testBit(FF_GAIN, ffFeatures)) {
		memset(&gain, 0, sizeof(gain));
		gain.type = EV_FF;
		gain.code = FF_GAIN;
		gain.value = 0xC000; /* [0, 0xFFFF]) */

		//printf("Setting master gain to 75%% ... ");
		fflush(stdout);
		if (write(fd, &gain, sizeof(gain)) != sizeof(gain)) {
		  perror("5.Error:");
		}
	}

	/* download a periodic sinusoidal effect */
	memset(&effects[0],0,sizeof(effects[0]));
	effects[0].type = FF_PERIODIC;
	effects[0].id = -1;
	effects[0].u.periodic.waveform = FF_SINE;
	effects[0].u.periodic.period = 100;	/* 0.1 second */
	effects[0].u.periodic.magnitude = 0x7fff;	/* 0.5 * Maximum magnitude */
	effects[0].u.periodic.offset = 0;
	effects[0].u.periodic.phase = 0;
	effects[0].direction = 0x4000;	/* Along X axis */
	effects[0].u.periodic.envelope.attack_length = 1000;
	effects[0].u.periodic.envelope.attack_level = 0x7fff;
	effects[0].u.periodic.envelope.fade_length = 1000;
	effects[0].u.periodic.envelope.fade_level = 0x7fff;
	effects[0].trigger.button = 0;
	effects[0].trigger.interval = 0;
	effects[0].replay.length = 20000;  /* 20 seconds */
	effects[0].replay.delay = 1000;

	fflush(stdout);
	if (ioctl(fd, EVIOCSFF, &effects[0]) == -1) {
		perror("6.Error:");
	}
	
	/* a strong rumbling effect */
	effects[4].type = FF_RUMBLE;
	effects[4].id = -1;
	effects[4].u.rumble.strong_magnitude = 0x8000;
	effects[4].u.rumble.weak_magnitude = 0;
	// effects[4].u.rumble.weak_magnitude = 0xc000;
	effects[4].replay.length = 400;
	effects[4].replay.delay = 0;

	fflush(stdout);
	if (ioctl(fd, EVIOCSFF, &effects[4]) == -1) {
		perror("3.Error");
	}

	/* a weak rumbling effect */
	effects[5].type = FF_RUMBLE;
	effects[5].id = -1;
	effects[5].u.rumble.strong_magnitude = 0;
	effects[5].u.rumble.weak_magnitude = 0xc000;
	effects[5].replay.length = 500;
	effects[5].replay.delay = 0;

	fflush(stdout);
	if (ioctl(fd, EVIOCSFF, &effects[5]) == -1) {
		perror("4.Error");
	}

	    int I = 4;
			memset(&play,0,sizeof(play));
			play.type = EV_FF;
			play.code = effects[I].id;
			play.value = 1;

			if (write(fd, (const void*) &play, sizeof(play)) == -1) {
				perror("Play effect");
				exit(1);
			}

			sleep(1);


	for (i=0; i<N_EFFECTS; ++i) {
		memset(&stop,0,sizeof(stop));
		stop.type = EV_FF;
		stop.code =  effects[i].id;
		stop.value = 0;
        
		if (write(fd, (const void*) &stop, sizeof(stop)) == -1) {
			perror("");
			exit(1);
		}
	}

	exit(0);
}

