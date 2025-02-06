# Sonar-Board-Game-Solver
<br>
<img src="https://cf.geekdo-images.com/GJIebwr7f57nohwY6idxDg__imagepagezoom/img/x2wfYgPqc66R5apO-MZumT91jWk=/fit-in/1200x900/filters:no_upscale():strip_icc()/pic3662558.jpg" width="100%" alt="sonar">
<img src="https://scontent.fbkk5-6.fna.fbcdn.net/v/t39.30808-6/463758184_3050695695086423_152137733213804601_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=0b6b33&_nc_ohc=A4xSFNoG0O0Q7kNvgFQ9vd3&_nc_oc=AdjyfO8QwRXo5q6ToFm-FXX1TLAhuunPh3gpBr8Ima_EJRcW4F-yi8EGccUajay2aIo&_nc_zt=23&_nc_ht=scontent.fbkk5-6.fna&_nc_gid=APvUx7eZOiB-YA3dKAHurC6&oh=00_AYC0PbDr0pwCvg-TfFKgl_021SrvofTltxS-GFXVvtfN1Q&oe=67A9E664" width="100%" alt="sonar">
Have you ever played "Sonar"? <br>
"Sonar" is a strategic board game that can play up to 8-player (each side 4-player), the more player you have the more likely your going to win. Because there are many task to do like calculate opponent possible location, planning maneuver, manage resource. But with this solver you could easily won against a 1v4. Because human can't calculate all opponent possible move like a machine. You just worried about maneuvering and managing resource, let the solver figuring out where you opponent submarine is. <br><br>
Not only in python, But i also implement this as a static website for anyone to use this solver through website link. <br>
Check it out here :  <br><br>



## Sonar Action
### Navigate
Move the submarine one space, but can't move to the location that you already been or island. <br><br>
<img src="https://github.com/user-attachments/assets/5b56a7e1-797e-417a-a1b0-52de56e5cd01" width="100%" alt="navigate">

### Drone
Drone is used to check weather opponent submarine is in that secction or not. <br><br>
<img src="https://github.com/user-attachments/assets/10b6be16-a0a6-4241-a416-d2dc47ba7866" width="100%" alt="drone">

### Sonar
Sonar is used to get a enemy position, but is that position combine with 1 truth and 1 lie, such as "E6" this mean opponent could be in a "Column E" or "Row 6". <br><br>
<img src="https://github.com/user-attachments/assets/02848903-b35b-4a6e-a8ad-1f37cff48cbe" width="100%" alt="sonar">

### Silent
Silent is used to move away from current positioon 4 space without telling your the other side which way you go. <br><br>
<img src="https://github.com/user-attachments/assets/4667a34f-71b3-4303-b020-cebcb1011611" width="100%" alt="silent">

### Repair
Repair is to repair you engine and reset walking path, but you have to reveal your submarine exact location to you opponent. <br><br>
<img src="https://github.com/user-attachments/assets/10c87efb-9d19-4d3c-98dc-554b623f07e9" width="100%" alt="repair">
<br><br>

For more detail check out this rulebooks : https://cdn.1j1ju.com/medias/64/53/3c-captain-sonar-rulebook.pdf 
<br><br>



## How to use a website


