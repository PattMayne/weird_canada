//written July 2015 Matt Payne    pattmayne.com
//for WeirdCanada.com

var player;

function play_track(player_id)
{
	if (player != null)
		{
			player.pause();
		}
	player = document.getElementById(player_id);
	player.play();

}

function pause_track()
{
	player.pause();
}