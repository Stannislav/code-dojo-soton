array oldbirds = random 30 birds
while(true)
{
	newbirds = new empty array
	loop: for bird in oldbirds
		newbird = updatebird(oldbirds, bird)
		newbirds.append(newbird)

	draw(newbirds)
	oldbirds = newbirds
	pause for 100ms
}



updatebird(oldbirds, bird):
	randomly move bird

updatebird_intelligent(oldbirds, bird):
	mindistance = 3
	maxdistance = 6
	1) not too near
	2) not too far
	3) same direction

	