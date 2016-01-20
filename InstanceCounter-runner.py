import click
from src.InstanceCounter import InstanceCounter


@click.command()
@click.option('--server', '-s', default="http://localhost:8585/bigdata/sparql",
              help='Uri to the sparql endpoint which stores the RDFS SubClass Information.')
@click.option('--user', '-u', default="admin", help='User for the sparql endpoint.')
@click.option('--password', '-p', default="dev98912011", help='Password for the sparql endpoint.')
@click.option('--n-processes', '-x', default="11",
              help='Number of processes to spawn simultaneously.')
@click.option('--file', '-f', default=None,
              help='Input file with classes to get counts for.')
@click.option('--target', '-t', default="./data/instance_count.db",
              help='Output sqlite db to save data into.')
@click.option('--log-level', '-l', default="WARN")
def main(server, user, password, log_level, n_processes, file, target):
    counter = InstanceCounter(server=server, sqlite_db=target, user=user, password=password,
                              n_processes=int(n_processes), log_level=log_level)

    if type(file) is list:
        for f in file:
            counter.count_all_instances(f)
    else:
        counter.count_all_instances(file)


if __name__ == '__main__':
    main()
