//written July 2015 Matt Payne    pattmayne.com
//for WeirdCanada.com

var player;

function play_track(player_id)
{
	player = document.getElementById(player_id);
	player.play();

}

function pause_track()
{
	player.pause();
}