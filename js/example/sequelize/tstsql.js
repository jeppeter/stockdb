import * as sqlite3 from 'sqlite3';
import * as util from 'util';
import * as jstracer from 'jstracer';
import * as extargsparse from 'extargsparse';

const trace_exit = exitcode => {
    jstracer.finish(err => {
        process.exit(exitcode);
    });
};

const command = `
	{
		"dbname|d" : null,
		"run" :  {
			"$" : "+"
		}
	}
`;

process.on('exit', exitcode => {
    trace_exit(exitcode);
});

process.on('uncaughtException', err => {
    jstracer.error('uncaughtException %s', err);
    trace_exit(3);
});

const parser = extargsparse.ExtArgsParse();

parser.load_command_line_string(command);
jstracer.init_args(parser);
const args = parser.parse_command_line();

jstracer.set_args(args);
if (args.verbose >= 3) {
    sqlite3.verbose();
}
if (args.dbname === null) {
    jstracer.error('please specify dbname by [--dbname|-d]');
    trace_exit(5);
}
const db = sqlite3.Database(args.dbname);

if (args.subcommand === 'run') {
	args.subnargs.forEach(sqlline => {
		db.run(sqlline,(err,rows) => {
			if (err !== undefined && err !== null) {
				jstracer.error(`query [${sqlline}] error [${err}]`);
				db.close();
				trace_exit(5);
			}
			jstracer.info(`row [${rows}]`);
			db.close();
			trace_exit(0);
		});
	});
}
