use clap::{Parser, Subcommand};
use rusqlite::{params, Connection, Result};
use serde::Deserialize;
use serde_json;
use serde_yaml;
use std::collections::HashMap;
use std::fs;

#[derive(Parser)]
#[command(name = "kguru")]
#[command(about = "A declarative and distributed Infrastructure as Code (IaC) manager")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Apply {
        #[arg(short, long)]
        file: String,
    },
}

#[derive(Debug, Deserialize)]
struct Manifest {
    name: String,
    actions: Vec<Action>,
}

#[derive(Debug, Deserialize)]
struct Action {
    // Renamed from action_type to name
    name: String,
    // Now parameters is a key/value map of strings.
    parameters: HashMap<String, String>,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Apply { file } => {
            let manifest_content =
                fs::read_to_string(file).expect("Failed to read the manifest file");
            let manifest: Manifest =
                serde_yaml::from_str(&manifest_content).expect("Failed to parse the manifest file");

            // Ensure the database is located in the current working directory.
            let current_dir = std::env::current_dir().expect("Failed to get current directory");
            let db_path = current_dir.join("var/log.sqlite");
            let conn = Connection::open(db_path)?;
            apply_manifest(&conn, &manifest)?;
        }
    }

    Ok(())
}

fn apply_manifest(conn: &Connection, manifest: &Manifest) -> Result<()> {
    for action in &manifest.actions {
        let serialized_parameters = serde_json::to_string(&action.parameters).map_err(|e| {
            rusqlite::Error::FromSqlConversionFailure(0, rusqlite::types::Type::Text, Box::new(e))
        })?;

        conn.execute(
            // Updated SQL statement using distinct column names: manifest and action_name.
            "INSERT INTO actions (manifest, action_name, parameters) VALUES (?1, ?2, ?3)",
            params![manifest.name, action.name, serialized_parameters],
        )?;
    }

    Ok(())
}
