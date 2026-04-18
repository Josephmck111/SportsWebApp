import { Component } from '@angular/core';
import { RouterOutlet, ActivatedRoute } from '@angular/router';
import { DataService } from './data.service';
import { Location } from '@angular/common';
import { WebService } from './web.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';


@Component({
  selector: 'team',
  standalone: true,
  imports: [RouterOutlet, CommonModule, FormsModule],
  providers: [DataService, WebService],
  templateUrl: './team.component.html',
  styleUrl: './team.component.css'
})


export class TeamComponent {
      // Properties for managing teams and user state.
      editingTeam: any = null; // Tracks the team being edited.
      team_list: any; // List of teams.
      isAuthenticated: boolean = false; // Indicates if the user is authenticated.
      isAdmin: boolean = false; // Indicates if the user has admin privileges.
      adminEmails: string[] = ['joem@glen.net', 'mckenna-j28@ulster.ac.uk', 'roryk@glen.net', 'adams@glen.net', 'davidd@glen.net', 'johnm@glen.net', 'stephenc@glen.net']; // List of admin emails.
  
      constructor( public dataService: DataService, private route: ActivatedRoute, private location: Location, private webService: WebService, public authService: AuthService) {}
  
      // Initialize the component.
      ngOnInit() {
        // Fetch team details based on the route parameter (team ID).
          this.webService.getTeam(this.route.snapshot.paramMap.get('id'))
            .subscribe( (response: any) => {
              this.team_list = [response];
          });
          // Check authentication state.
          this.authService.isAuthenticated$.subscribe({
            next: (isAuthenticated) => {
              this.isAuthenticated = isAuthenticated;
        
              // Check if user is an admin
              if (isAuthenticated) {
                this.authService.user$.subscribe({
                  next: (user) => {
                    this.isAdmin = this.adminEmails.includes(user?.email || '');
                  },
                  error: (error) => {
                    console.error('Failed to retrieve user details:', error);
                  },
                });
              }
            },
            error: (error) => {
              console.error('Failed to determine authentication status:', error);
            },
          });
      }

      // Navigate back to the previous page.
      goBack(): void {
        this.location.back();
      }

      // Toggle edit mode for the specified team.
      toggleEditMode(team: any): void {
        if (this.editingTeam === team) {
            this.editingTeam = null; // Exit edit mode 
        } else {
            this.editingTeam = team; // Enter edit mode for the selected team
        }
      }

      // Save changes to the specified team.
      saveChanges(team: any): void {
        if (!team._id) {
            alert('Team ID is missing!');
            return;
        }

        this.webService.updateTeam(team).subscribe({
            next: () => {
                alert('Team updated successfully!');
                this.editingTeam = null; // Exit edit mode
            },
            error: (err) => {
                console.error('Error updating team:', err);
                alert('Failed to update team! Please try again.');
            }
        });
      }

      // Delete the specified team by its ID.
      deleteTeam(userId: string): void {
        if (!confirm('Are you sure you want to delete this team?')) {
            return; // User canceled the delete action
        }

        this.webService.deleteTeam(userId).subscribe({
            next: () => {
                alert('Team deleted successfully!');
                this.goBack();
            },
            error: (err) => {
                console.error('Failed to delete team:', err);
                alert('Failed to delete team!');
            }
        });
      } 

      
 }
