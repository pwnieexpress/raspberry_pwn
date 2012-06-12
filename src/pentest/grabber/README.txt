Grabber v0.1
------------

Grabber is a web application which try to be as useful as possible ie allows:
- back box testing
- hybrid analysis
- javscript source code checker

The tool aims to be quite generic, so even if I use PHP-SAT as php source code analyzer, you could use
a java source code analyzer for your website. You can also add some attacks pattern you found etc.
For more information go to the website.

Contact
-------

  author:  Romain Gaucher
  website: http://rgaucher.info/beta/grabber
  email:   r@rgaucher.info


What would be cool to have/integrate (except no more bugs) ?
------------------------------------------------------------

  + Core:
         Support of cookies, Http Auth
  + XSS:
         Plug in a JavaScript interpreter (spidermonkey still compiled ^^)
  + Session:
         Report the SessionID
         Report on the randomness of the sessions id (statistical distribution)
  + Cookies:
         Analyze the cookies (look for secure, HttpOnly etc.)
  + Passwords:
         Passwords hash analyzer ?
         Is it enough secure...
  + SSL/TLS:
         ???
  + Configuration report:
         Look at the CVE/NVD give the report if there is such a configuration information
         ASP / PHP / MySQL versions
         APACHE / IIS etc.
  + Log Visualisation Systems
         XSS ?

Disclaimer
----------

I should write a disclaimer here ? Hum, I'm not responsible of any results/trouble/nuclear punch in
your website after the utilisation of Grabber.
This soft performs only attack patterns it should not create anything wrong in your website (except if it's a really crap).

During the hybrid analysis, there could be some trouble... I suggest you to save the files even if everything is done in the
./local/ directory (I copy the source files in the ./local/current and the analysis output are in the ./local/analyzed)

Of course, if the Grabber does not find any vulnerability, it doesn't mean at all that there is none; only that grabber found
nothing. <disgression>Even if you use Grabber or whatever tool you want, you cannot have a website 100% secure...
it's impossible</disgression>

Licence
-------

I will put the BSD Licence stuffs. But still, it is under the modified BSD licence.
