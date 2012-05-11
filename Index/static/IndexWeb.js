function toggle_div(divid)
{
	if(document.getElementById(divid).style.display=='block')
	{
		document.getElementById(divid).style.display='none';
	}
	else
	{
		document.getElementById(divid).style.display='block';
	}
}