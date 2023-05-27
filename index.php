<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alive...</title>
</head>
<body>
    <?php
        $output = shell_exec("python bot_PIU.py");
        echo $output;
    ?>
    <p>Nothing to see here, the bot is up and alive.</p>
</body>
</html>