$(document).ready(function(){
	console.log('working!');
	$('#likes').click(function(){
		var catid;
		catid = $(this).attr("data-catid");
		console.log(catid);
		$.get('/rango/like_category', {category_id: catid}, function(data){
		$('#like_count').html(data);
		$('#likes').hide();
	   });
	});
});
