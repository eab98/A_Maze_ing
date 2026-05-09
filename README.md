*This project has been created as part of the 42 curriculum by lmoreau and bel-azzo*

# [A-MAZE-ING]
> *“A labyrinth is not a place to be lost, but a path to be found.”*

### Description: 

Le projet A-Maze-ing consiste à concevoir un programme capable de générer des labyrinthes parfaits (sans cycles et où chaque point est accessible) et de proposer, le cas échéant, une solution pour les résoudre. L'objectif principal est de manipuler des algorithmes de théorie des graphes et de gérer des structures de données complexes tout en respectant des contraintes de performance et de configuration.

### Instructions : 
installation : Clonez le dépôt et rendez-vous à la racine du projet : git clone `https://github.com/votre-repo/a-maze-ing.git`
`cd a-maze-ing`

exécution : 
`make run`

format de la config : `./a_maze_ing.py config.txt`

Format complet du config file (toutes les clés, types, exemples)
Algorithme de génération choisi et justification du choix // plus facile a utiliser: genere et cherche en meme temps + plus joli 
Code réutilisable : comment importer MazeGenerator, exemple d'usage, accès à la solution

### Gestion d'équipe : 
bel-azzo = Algorithm part // lmoreau = Visual part
Nous avons répartit la réalisation du projet sur 7 jours. 

bien marcher : bonne repartition, aide mutuelle, cooperation, juste parfait   
a ameliorer : 

**--------------------------------------------------------------------------------------------------------------------------**

<details open>
  <summary><b>Planning</b></summary>
  <br>
	<table style="width: 100%;">
	<tr>
		<td style="width: 50%; vertical-align: top;">
		<h3>Bel-azzo</h3>
		<ul>
			<li>Jour 1 : Structure Cell + parsing</li>
			<li>Jour 2 : Interface MazeGenerator</li>
			<li>Jour 3 : Algorithme DFS + gestion seed</li>
			<li>Jour 4 : Gestion erreur 3*3 </li>
			<li>Jour 5 : Pattern "42"</li>
			<li>Jour 6 : BFS solver</li>
			<li>Jour 7 : Fichier sortie hex + Package pip/build.whl</li>
		</ul>
		</td>
		<td style="width: 40%; vertical-align: top;">
		<h3>Lmoreau</h3>
		<li>Jour 1 : Wireframe ASCII</li>
		<li>Jour 2 : Class MazeRenderer</li>
		<li>Jour 3 : curses init + dessin murs</li>
		<li>Jour 4 : Affichage Entry/Exit</li>
		<li>Jour 5 : Pattern "42"</li>
		<li>Jour 6 : Overlay chemin + "42"</li>
		<li>Jour 7 : Read.me</li>
		</td>
	</tr>
	</table>
</details>

**--------------------------------------------------------------------------------------------------------------------------**


### Resources : 

<details open>
  <br>
	<table style="width: 100%;">
	<tr>
		<td style="width: 50%; vertical-align: top;">
		<h4>Algo part</h4>
		<ul>
			<li>https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742</li>
			<li>https://dqwertyc.github.io/unity-maze-generator/</li>
			<li>https://www.w3schools.com/python/</li>
			<li>Jhttps://docs.python.org/3.12</li>
		</ul>
		</td>
		<td style="width: 50%; vertical-align: top;">
		<h4>Visual part</h4>
		<li>https://docs.python.org/3/howto/curses.html</li>
		<li>https://realpython.com/ref/stdlib/curses/</li>
		<li>https://talks.freelancerepublik.com/regles-ecrire-readme-md-github/</li>
		</td>
	</tr>
	</table>
</details>


> This is the way 