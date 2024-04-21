use std::path::PathBuf;

use clap::{arg, command, value_parser};

fn main() {
    let matches = command!().arg(
        arg!(
            -c --config <FILE> "Load config from <FILE>"
        )
        .required(false)
        .value_parser(value_parser!(PathBuf)),
    );
}
