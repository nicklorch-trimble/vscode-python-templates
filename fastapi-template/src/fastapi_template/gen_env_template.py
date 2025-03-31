import argparse
from .settings import Settings

def generate_env_template(output_path: str = ".env.template") -> None:
    """
    Generate a template .env file based on the Settings class.

    Parameters
    ----------
    output_path : str
        Path where the .env.template file will be saved. Default is ".env.template".

    Returns
    -------
    None
        Writes the template to the specified file.
    """


    # Create a settings instance with default values
    settings = Settings()

    # Get the environment prefix from model_config
    env_prefix = settings.model_config.get('env_prefix', '').upper()

    # Generate the template content
    template_lines = []
    template_lines.append("# Template environment configuration for tid-sample-api")
    template_lines.append("# Copy this file to .env and modify as needed")
    template_lines.append("")

    # Get fields from Settings class annotations
    for field_name, field_type in Settings.__annotations__.items():
        if field_name != 'model_config' and not field_name.startswith('_'):
            # Get the default value from the settings instance
            field_value = getattr(settings, field_name, '')

            # Add the field to the template
            template_lines.append(f"# {field_name} ({field_type.__name__})")
            template_lines.append(f"{env_prefix}{field_name.upper()}={field_value}")
            template_lines.append("")

    # Write to file
    with open(output_path, "w") as f:
        f.write("\n".join(template_lines))

    print(f"ENV template file generated at: {output_path}")

def main():
    """Command line interface to generate .env.template file."""

    parser = argparse.ArgumentParser(description="Generate a .env.template file from Settings")
    parser.add_argument("--output", "-o", default=".env.template",
                        help="Output file path (default: .env.template)")

    args = parser.parse_args()
    generate_env_template(args.output)

if __name__ == "__main__":
    main()