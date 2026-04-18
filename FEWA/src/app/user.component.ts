import { Component } from '@angular/core';
import { RouterOutlet, ActivatedRoute } from '@angular/router';
import { DataService } from './data.service';
import { Location } from '@angular/common';
import { WebService } from './web.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'user',
  standalone: true,
  imports: [RouterOutlet, CommonModule, FormsModule],
  providers: [DataService, WebService],
  templateUrl: './user.component.html',
  styleUrl: './user.component.css'
})


export class UserComponent { 
      // Properties for managing user-related operations and state.
      user_list: any; // Holds the list of users.
      editingUser: any = null; // Tracks the user currently in edit mode.
      isAuthenticated: boolean = false; // Tracks whether the user is logged in.
      isAdmin: boolean = false; // Tracks whether the user has admin privileges.
      adminEmails: string[] = ['joem@glen.net', 'mckenna-j28@ulster.ac.uk', 'roryk@glen.net', 'adams@glen.net', 'davidd@glen.net', 'johnm@glen.net', 'stephenc@glen.net']; // List of admin emails.
  
      constructor( public dataService: DataService, private route: ActivatedRoute, private location: Location, private webService: WebService, private router: Router, public authService: AuthService) {}
  
      // Initialize the component.
      ngOnInit() {
        // Fetch the user based on the route parameter (user ID).
        this.webService.getUser(this.route.snapshot.paramMap.get('id'))
          .subscribe( (response: any) => {
            this.user_list = [response]; // Store user data in a list.
          });

          // Subscribe to authentication status and check admin privileges.
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

      // Toggle the edit mode for a specific user.
      toggleEditMode(user: any): void {
        if (this.editingUser === user) {
            this.editingUser = null; // Exit edit mode if the same user is clicked again
        } else {
            this.editingUser = user; // Enter edit mode for the selected user
        }
      }

      // Save changes made to a user.
      saveChanges(user: any): void {
        // Validate user ID presence
        if (!user._id) {
            alert('User ID is missing!');
            return;
        }
    
        // Call the WebService to update the user
        this.webService.updateUser(user).subscribe({
            next: () => {
                alert('User updated successfully!');
                this.editingUser = null; // Exit edit mode
            },
            error: (err) => {
                console.error('Error updating user:', err);
                alert('Failed to update user! Please check your input or try again later.');
            }
        });
      }
    
      // Cancel the edit mode without saving changes.
      cancelEdit(): void {
        this.editingUser = null; // Exit edit mode without saving
      }

      // Delete a user based on their ID.
      deleteUser(userId: string): void {
        if (!confirm('Are you sure you want to delete this user?')) {
            return; // User canceled the delete action
        }

        // Call the WebService to delete the user.
        this.webService.deleteUser(userId).subscribe({
            next: () => {
                alert('User deleted successfully!');
                this.goBack(); // Navigate back after successful deletion.
            },
            error: (err) => {
                console.error('Failed to delete user:', err);
                alert('Failed to delete user!');
            }
        });
      } 
}
