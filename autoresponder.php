<?php
    $mailbox = $_POST['mailbox'];
    $mail = $_POST['mail'];
    ob_start();
    passthru('/usr/bin/python /path/to/autoresponder.py "' . $mail . '"');
    echo ob_get_clean();
?>
