/* modified from https://gist.github.vom/hadess/6847281
 * by mcncm, to accommodate my machine and remove unwanted dependencies
 *
 * gcc -o tmp `pkg-config --libs --cflags glib-2.0` tmp.c
 *
 */

#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

const char levels[] = {
	0x01,
	0x41,
	0x81
};

void emitError(const char *errorSource) {
  // a trivial error-message function
  printf("Exited %s with error: %s\n", errorSource, strerror(errno));
  //_exit(EXIT_FAILURE);
}

static void
usage (char **argv)
{
	printf ("%s [level]\n", argv[0]);
	printf ("where level is between 0 and 2\n");
}

int main (int argc, char **argv)
{
	int fd;
	int level;

	if (argc < 2) {
		usage (argv);
		return 1;
	}
	level = atoi(argv[1]);
	if (level < 0 || level > 2) {
		usage (argv);
		return 1;
	}

	fd = open ("/sys/kernel/debug/ec/ec0/io", O_RDWR);
	//fd = open ("./test.txt", O_RDWR);
	if (fd < 0)
    emitError("open");
	if (lseek (fd, 0xd, SEEK_CUR) < 0)
    emitError("lseek");
	if (write (fd, &levels[level], 1) < 0) //&levels[level], 1) < 0)
    emitError("write");
	if (close (fd) < 0)
    emitError("close");

	return 0;
}
