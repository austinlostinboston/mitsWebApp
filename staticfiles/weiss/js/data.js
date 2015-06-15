function swingBar(pos, neg, neu, canvas) {
    var block_size = 5;
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    var total_length = pos + neg + neu;
    ctx.font = "15px Arial";
    ctx.fillStyle = "#FF0000";
    ctx.fillRect(20,20,neg * block_size,20);
    ctx.stroke();
    ctx.strokeText(neg, 20 + neg * block_size + 5, 40)

    ctx.fillStyle = "#888888";
    ctx.fillRect(20, 50, neu * block_size, 20);
    ctx.stroke();
    ctx.strokeText(neu, 20 + neu * block_size + 5, 70)

    ctx.fillStyle = "#006600";
    ctx.fillRect(20, 80, pos * block_size, 20);
    ctx.stroke();
    ctx.strokeText(pos, 20 + pos * block_size + 5, 100)

    ctx.beginPath();
    ctx.moveTo(20,20);
    ctx.lineTo(20,100);
    ctx.stroke();
}
