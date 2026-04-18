import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatchesComponent } from './matches.component';
import { NavComponent } from './nav.component';
import { DataService } from './data.service';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MatchesComponent, NavComponent],
  providers: [DataService],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})


export class AppComponent {
  title = 'matchFE';

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataService.populateComments();
  }
}
