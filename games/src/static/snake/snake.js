var random = function (min, max) {k = Math.floor(Math.random() * (max - min) + min);
	return (Math.round( k / size) * size);
	}

var newApple = function () {
	apple = [random(0, innerHeight - size),random(0, innerHeight - size)];
	}

var	newB = function () {
	sBody = [{x: 3 * size,y: 3 * size}, {x: 4 * size, y: 3 * size}, {x: 5 * size,y: 3 * size}];
	}

var score = 0;
var width1 = (innerHeight - 200);
var corner_x = (innerWidth - width1) / 2;
var corner_y = (innerHeight - width1) / 2;
var gP = document.getElementById('gP'), //Достаем canvas
	g = gP.getContext('2d'), //Получаем "контакс" (методы для рисования в canvas) //Сохраняем для удобства
	sBody = null, //Начально тело змейки - два элемента
	direction = 'right';
	apple = null, //Яблоко, массив, 0 элемент - x, 1 элемнт - y
	size = Math.round(width1 / 20), newB(); newApple(); //Создаем змейку

gP.width = innerWidth; //Сохранем четкость изображения, выставив полную ширину экрана
gP.height = innerHeight;
width1 = 20 * size;

var playing = setInterval(function(){

	if (apple[0] + size >= width1 || apple[1] + size >= width1){
		newApple();
	}
	g.clearRect(0,0,gP.width,gP.height);
	g.fillStyle = "white";
	g.fillRect(corner_x + 1,corner_y + 1, width1, width1);
	g.fillStyle = "red";
	g.fillRect(apple[0] + corner_x, apple[1] + corner_y, size, size);
	g.fillStyle = "black";
	g.fillRect(corner_x - 1,corner_y - 1, 2, width1 +2);
	g.fillRect(corner_x - 1, corner_y - 1, width1 + 2, 2);
	g.fillRect(corner_x + width1 -1, corner_y -1, 2, width1 +2);
	g.fillRect(corner_x - 1, corner_y + width1 -1, width1 +2, 2);
	g.fillStyle = "blue";
	sBody.forEach(function(el, i){
		if (el.x == sBody[sBody.length - 1].x && el.y == sBody[sBody.length - 1].y && i < sBody.length - 1){
			alert("Gameover, your score: " + score);
			clearInterval(playing);
		}
	});

	var head = sBody[0], newhead = {x: head.x, y: head.y}, tail = sBody[sBody.length - 1]; // сохраняем хвост и голову змейки
	if (direction == 'right'){
		newhead.x = tail.x + size, newhead.y = Math.round(tail.y / size) * size; //right
	}
	if (direction == 'down'){
		newhead.y = tail.y + size, newhead.x = Math.round(tail.x / size) * size; // down
	}
	if (direction == 'left'){
		newhead.x = tail.x - size, newhead.y = Math.round(tail.y / size) * size; // left
	}
	if (direction == 'up'){
		newhead.y = tail.y - size, newhead.x = Math.round(tail.x / size) * size; // up
	} 
	sBody.push(newhead); //Добавляем хвост после головы с новыми координатами
	sBody.splice(0,1); //Удаляем хвост
	//Отрисовываем каждый элемент змейки
	sBody.forEach(function(part, i){
		if (direction == 'right' && part.x > (Math.round(width1 / size) - 1) * size){
			part.x = 0;
		}
		if (direction == 'down' && part.y > (Math.round(width1 / size) - 1) * size){
			part.y = 0;
		}
		if (direction == 'left' && part.x < 0){
			part.x = (Math.round(width1 / size) - 1) * size;
		}
		if (direction == 'up' && part.y < 0){
			part.y = (Math.round(width1 / size) - 1) * size;
		} 
		if (part.x == apple[0] && part.y == apple[1]){
			newApple();
			score = score + 5;
			sBody.unshift({x: newhead.x - size, y:tail.y});
		}
		g.fillRect(part.x + corner_x, part.y + corner_y, size, size);
	});
}, 1000/20);

onkeydown = function (e) {
		var k = e.keyCode;
		if ([38,39,40,37].indexOf(k) >= 0) 
			e.preventDefault();
		if (k == 39 && direction != 3 && sBody[sBody.length - 2].x+size != sBody[sBody.length - 1].x && sBody[sBody.length - 2].y != sBody[sBody.length - 1].y) direction = 'right'; 
		if (k == 40 && direction != 4 && sBody[sBody.length - 2].x != sBody[sBody.length - 1].x && sBody[sBody.length - 2].y-size != sBody[sBody.length - 1].y) direction = 'down'; 
		if (k == 37 && direction != 1 && sBody[sBody.length - 2].x-size != sBody[sBody.length - 1].x && sBody[sBody.length - 2].y != sBody[sBody.length - 1].y) direction = 'left'; 
		if (k == 38 && direction != 2 && sBody[sBody.length - 2].x != sBody[sBody.length - 1].x && sBody[sBody.length - 2].y+size != sBody[sBody.length - 1].y) direction = 'up'; 
	};