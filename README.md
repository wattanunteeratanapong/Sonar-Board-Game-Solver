# Sonar Board Game Solver
<br>
<img src="https://cf.geekdo-images.com/GJIebwr7f57nohwY6idxDg__imagepagezoom/img/x2wfYgPqc66R5apO-MZumT91jWk=/fit-in/1200x900/filters:no_upscale():strip_icc()/pic3662558.jpg" width="100%" alt="sonar">
<img src="https://github.com/user-attachments/assets/345dec92-a872-401d-beee-42829ae4cfaf" width="100%" alt="sonar">

Have you ever played "Sonar"? <br>
"Sonar" is a strategic board game that can play up to 8-player (each side 4-player), the more player you have the more likely your going to win. Because there are many task to do like figuring out opponent submarine location, planning maneuvering, manage resource, torpedo your opponent submarine. But with this solver you could easily won against a 1v4. Because human can't calculate all opponent possible move like a machine. You just worried about maneuvering and managing resource etc. and Let the solver figuring out where you opponent submarine is. <br><br>



## Sonar Action
### Navigate
Move the submarine one space, but can't move to the location that you already been or island. <br><br>
<img src="https://github.com/user-attachments/assets/5b56a7e1-797e-417a-a1b0-52de56e5cd01" width="100%" alt="navigate">

### Drone
Drone is used to check weather opponent submarine is in that section or not. <br><br>
<img src="https://github.com/user-attachments/assets/10b6be16-a0a6-4241-a416-d2dc47ba7866" width="100%" alt="drone">

### Sonar
Sonar is used to get a enemy position, but is that position combine with 1 truth and 1 lie, such as "E6" this mean opponent could be in a "Column E" or "Row 6". <br><br>
<img src="https://github.com/user-attachments/assets/02848903-b35b-4a6e-a8ad-1f37cff48cbe" width="100%" alt="sonar">

### Silent
Silent is used to move away from current positioon 4 space without telling your the other side which way you go. <br><br>
<img src="https://github.com/user-attachments/assets/4667a34f-71b3-4303-b020-cebcb1011611" width="100%" alt="silent">

### Repair
Repair is to repair you engine and reset walking path, but you have to reveal your submarine sector to you opponent. <br><br>
<img src="https://github.com/user-attachments/assets/10c87efb-9d19-4d3c-98dc-554b623f07e9" width="100%" alt="repair">
<br>

For more detail check out this rulebooks : https://cdn.1j1ju.com/medias/64/53/3c-captain-sonar-rulebook.pdf 
<br><br>
