<?php
try {
    $bdd = new PDO('mysql:host=localhost;dbname=flaskcontacts', 'renato', 'Jota.1584');
} catch(Exception $e) {
    exit('Unable to connect to database.');
}
$id = $_POST['id'];
$sql = "DELETE from eventos WHERE id=".$id;
$q = $bdd->prepare($sql);
$q->execute();
?>