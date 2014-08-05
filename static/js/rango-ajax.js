$(document).ready(function(){
	console.log('working!');
	//like button onclick function
	$('#likes').click(function(){
		var catid;
		catid = $(this).attr("data-catid");
		console.log(catid);
		$.get('/rango/like_category', {category_id: catid}, function(data){
		$('#like_count').html(data);
		$('#likes').hide();
	   });
	});
	//suggest input keyup function
	$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/rango/suggest_category/', {suggestion: query}, function(data){
			$('#cats').html(data);
		});
	});
});
