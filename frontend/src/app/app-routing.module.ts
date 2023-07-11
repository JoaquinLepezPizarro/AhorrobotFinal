import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { QuienesSomosComponent } from './componentes/quienes-somos/quienes-somos.component';
import { InicioComponent } from './componentes/inicio/inicio.component';
import { ContactoComponent } from './componentes/contacto/contacto.component';
import { ErrorComponent } from './componentes/error/error.component';

const routes: Routes = [
  { path: "", redirectTo: "/inicio", pathMatch: "full"},
  { path: "inicio", component: InicioComponent},
  { path: "quienesSomos", component: QuienesSomosComponent},
  { path: "contacto", component: ContactoComponent},
  { path: "**", component: ErrorComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

