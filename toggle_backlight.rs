/*
Keyboard backlight setter for Lenovo X1 Carbon
Author: mcncm, 2019

I use this to provide a hardware light indicator of when my environment is
in a non-defualt mode, e.g. when my window manager is in a "resize" mode.

Usage:
$ ./toggle_backlight 0      off
$ ./toggle_backlight 1      low
$ ./toggle_backlight 2      high

Needs root privileges to write to the kernel file containing this setting.
e.g. compile and chown to root:
$ rustc toggle_backlight.rs
$ sudo chown root:root toggle_backlight
$ sudo chmod +s toggle_backlight
*/


use std::io::SeekFrom;
use std::io::prelude::*;
use std::error::Error;
use std::env;
use std::process;

const LEVELS: [u8; 3] = [0x01, 0x41, 0x81];
const WRITE_POS: u64 = 0xd;
const MIN_LEVEL: usize = 0;
const MAX_LEVEL: usize = 2;
const KERNEL_FILE: &'static str = "/sys/kernel/debug/ec/ec0/io";

// Signature too long?
fn write_kernel_file(filename: &'static str, bl_level: usize) -> Result<(), Box<dyn Error>> {
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .read(true)
        .open(filename)?;

    file.seek(SeekFrom::Start(WRITE_POS))?;
    file.write(&[LEVELS[bl_level]])?;  // Awkward: better way to get single-u8 slice?

    Ok(())
}

fn main() {
    let mut args = env::args();
    args.next();

    let bl_level: usize = match args.next() {
        Some(v) => v.parse().unwrap_or_else(|err| {
            eprintln!("Problem parsing arguments: {}", err);
            process::exit(1);
        }),
        None => {
            eprintln!("Enter a numeric level between {} and {}.", MIN_LEVEL, MAX_LEVEL);
            process::exit(1);
        }
    };

    write_kernel_file(KERNEL_FILE, bl_level).unwrap_or_else(|err| {
        eprintln!("Problem writing kernel file: {}", err);
        process::exit(1);
    });
}
