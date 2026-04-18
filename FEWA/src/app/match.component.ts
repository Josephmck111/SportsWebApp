import { Component } from '@angular/core';
import { ActivatedRoute, RouterOutlet } from '@angular/router';
import { DataService } from './data.service';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';
import { WebService } from './web.service';
import { Location } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'match',
  standalone: true,
  imports: [RouterOutlet, CommonModule, ReactiveFormsModule, FormsModule],
  providers: [DataService, WebService],
  templateUrl: './match.component.html',
  styleUrls: ['./match.component.css']
})
export class MatchComponent {
  // Define properties for managing matches, comments, videos, and authentication state.
  match_list: any[] = []; // List of all matches.
  editingMatch: any = null; // Track which match is being edited.
  commentForm!: FormGroup; // Form for adding new comments.
  comment_list: any[] = []; // List of comments for a match.
  selectedFile: File | null = null; // File selected for upload.
  videos: any[] = []; // List of uploaded videos.
  editingComment: any = null; // Track which comment is being edited.
  isAdmin: boolean = false; // Flag to check admin privileges.
  isAuthenticated: boolean = false; // Check if the user is authenticated.
  uploadedVideoUrl: string | null = null; // URL of the uploaded video.
  matchId: string | null = null; // ID of the selected match.
  adminEmails: string[] = ['joem@glen.net', 'mckenna-j28@ulster.ac.uk', 'roryk@glen.net', 'adams@glen.net', 'davidd@glen.net', 'johnm@glen.net', 'stephenc@glen.net']; // Admin emails.

  constructor(
    public dataService: DataService,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    public authService: AuthService,
    private webService: WebService,
    private location: Location
  ) {}

  // Initialize the component.
  ngOnInit(): void {
    // Initialize the comment form with validators.
    this.commentForm = this.formBuilder.group({
      username: ['', Validators.required],
      text: ['', Validators.required]
    });
    
    // Fetch the match ID from the route and fetch match details if present.
    this.matchId = this.route.snapshot.paramMap.get('id');
    if (this.matchId) {
      this.getMatchDetails(this.matchId); // Fetch match details
      this.getComments(this.matchId); // Fetch comments for the match
    }
    
    // Check authentication state and set admin privileges.
    this.authService.isAuthenticated$.subscribe({
      next: (isAuthenticated) => {
        this.isAuthenticated = isAuthenticated;
        if (isAuthenticated) {
          this.authService.user$.subscribe({
            next: (user) => {
              this.isAdmin = this.adminEmails.includes(user?.email || '');
            },
            error: (error) => {
              console.error('Failed to retrieve user details:', error);
            }
          });
        }
      },
      error: (error) => {
        console.error('Failed to determine authentication status:', error);
      }
    });
  }

  // Fetch video details for the given match ID.
  fetchVideo(id: string): void {
    this.webService.getMatch(id).subscribe({
      next: (response) => {
        this.uploadedVideoUrl = response.VideoURL; // Use the VideoURL as is
        console.log('Fetched video URL:', response.VideoURL);
      },
      error: (error) => {
        console.error('Failed to fetch video URL:', error);
      }
    });
  }
  
  // Handle file selection for video upload.
  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  // Upload the selected video for the match.
  uploadVideo(): void {
    if (!this.selectedFile) {
      console.warn('No file selected for upload.');
      alert('Please select a file to upload.');
      return;
    }
  
    const formData = new FormData();
    formData.append('file', this.selectedFile);
  
    if (!this.matchId) {
      console.error('Match ID is missing.');
      return;
    }
  
    this.webService.uploadVideo(this.matchId, formData).subscribe({
      next: (response) => {
        this.uploadedVideoUrl = response.video_url; 
        console.log('Video uploaded successfully:', response.video_url);
      },
      error: (error) => {
        console.error('Failed to upload video:', error);
      },
      complete: () => {
        console.log('Video upload process complete.');
      }
    });
  }
  
  // Fetch match details for the given ID.
  getMatchDetails(id: string): void {
    this.webService.getMatch(id).subscribe({
      next: (response) => {
        this.match_list = [response]; 
        this.uploadedVideoUrl = response.VideoURL; 
        console.log('Match details and video URL fetched:', response.VideoURL);
      },
      error: (error) => {
        console.error('Failed to fetch match details:', error);
      }
    });
  }

  // Delete the video associated with the match.
  deleteVideo(): void {
    if (!this.matchId) {
      console.error('Match ID is missing.');
      return;
    }
  
    this.webService.deleteVideo(this.matchId).subscribe({
      next: (response) => {
        this.uploadedVideoUrl = null; 
        console.log('Video deleted successfully:', response.message);
      },
      error: (error) => {
        console.error('Failed to delete video:', error);
      },
    });
  }

  // Fetch comments for the given match ID.
  getComments(matchId: string): void {
    this.webService.getComments(matchId).subscribe({
        next: (response) => {
            // Attach the comments directly to the corresponding match in match_list
            const match = this.match_list.find((m: any) => m._id === matchId);
            if (match) {
                match.comments = response; // Add comments to the match
            }
            console.log('Comments fetched and attached:', response);
        },
        error: (error) => {
            console.error('Failed to fetch comments:', error);
        }
    });
  }

  // Submit a new comment for the match.
  onSubmit(): void {
    const matchId = this.route.snapshot.paramMap.get('id');
    if (!matchId) {
      console.warn('No match ID found.');
      return;
    }
  
    this.webService.postComment(matchId, this.commentForm.value).subscribe({
      next: () => {
        this.commentForm.reset();
        console.log('Comment submitted successfully.');
        // Fetch updated comments to refresh UI
        this.getComments(matchId);
      },
      error: (error) => {
        console.error('Failed to post comment:', error);
      },
    });
  }
  
  // Toggle edit mode for a match.
  toggleEditMode(match: any): void {
    if (this.editingMatch === match) {
        this.editingMatch = null; // Exit edit mode if the same match is clicked again
    } else {
        this.editingMatch = match; // Enter edit mode for the selected match
    }
  }

  // Save the changes made to a match.
  saveChanges(match: any): void {
    if (!match._id) {
        alert('Match ID is missing!');
        return;
    }

    this.webService.updateMatch(match).subscribe({
        next: () => {
            alert('Match updated successfully!');
            this.editingMatch = null; // Exit edit mode
        },
        error: (err) => {
            console.error('Error updating match:', err);
            alert('Failed to update match! Please try again.');
        }
    });
  }

  // Check if a form control is invalid and touched.
  isInvalid(control: string): boolean {
    return this.commentForm.controls[control].invalid && this.commentForm.controls[control].touched;
  }

  // Check if a form control is untouched.
  isUntouched(): boolean {
    return this.commentForm.controls['username'].pristine || this.commentForm.controls['text'].pristine;
  }

  // Check if the comment form is incomplete.
  isIncomplete(): boolean {
    return this.isInvalid('username') || this.isInvalid('text') || this.isUntouched();
  }

  // Navigate back to the previous location.
  goBack(): void {
    this.location.back();
  }

  // Delete a match by its ID.
  deleteMatch(userId: string): void {
    if (!confirm('Are you sure you want to delete this match?')) {
        return; // User canceled the delete action
    }

    this.webService.deleteMatch(userId).subscribe({
        next: () => {
            alert('Match deleted successfully!');
            this.goBack();

        },
        error: (err) => {
            console.error('Failed to delete match:', err);
            alert('Failed to delete match!');
        }
    });
  } 

  // Delete a comment by match and comment ID.
  deleteComment(matchId: string, commentId: string): void {
    if (!confirm('Are you sure you want to delete this comment?')) {
        return; // User canceled the delete action
    }

    this.webService.deleteComment(matchId, commentId).subscribe({
        next: () => {
            alert('Comment deleted successfully!');
            // Refresh the comments list after deletion
            this.getComments(matchId);
        },
        error: (err) => {
            console.error('Failed to delete comment:', err);
            alert('Failed to delete comment!');
        }
    });
}


}
