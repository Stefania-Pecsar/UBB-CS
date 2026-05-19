using System.Runtime.InteropServices.JavaScript;
using Lab_10.Console;
using Lab_10.Domain;
using Lab_10.Repository;
using Lab_10.Service;

Repository<String,Team> teamFileRepository = new TeamFileRepository("C:\\Users\\FANE\\Desktop\\fac\\AN 2\\MAP\\MAP\\Lab_10\\Lab_10\\files\\teams.txt");
Repository<String, Player> playerFileRepository = new PlayersFileRepository("C:\\Users\\FANE\\Desktop\\fac\\AN 2\\MAP\\Lab_10\\Lab_10\\files\\players.txt");
Repository<String,Match> matchFileRepository = new MatchFileRepository("C:\\Users\\FANE\\Desktop\\fac\\AN 2\\MAP\\Lab_10\\Lab_10\\files\\matches.txt");
Repository<String, ActivePlayer> activePlayerFileRepository = new ActivePlayersFileRepository("C:\\Users\\FANE\\Desktop\\fac\\AN 2\\MAP\\Lab_10\\Lab_10\\files\\activePlayers.txt");

Service service = new Service(teamFileRepository, playerFileRepository, matchFileRepository, activePlayerFileRepository);

ConsoleApp console = new ConsoleApp(service);

console.run();