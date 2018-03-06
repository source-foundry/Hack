<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <!-- Declare Hack a monospace font -->
  <alias>
    <family>Hack</family>
    <default><family>monospace</family></default>
  </alias>
  <!-- if this file is put in user’s configuration, unset sans-serif family -->
  <match>
    <test compare="eq" name="family">
        <string>Hack</string>
    </test>
    <test compare="eq" name="family">
        <string>sans-serif</string>
    </test>
    <edit mode="delete" name="family"/>
  </match>
</fontconfig>
