import { Component, OnInit } from '@angular/core';
import {AppService} from '../../services/app.service';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-inicio',
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.scss']
})

export class InicioComponent implements OnInit{
  productos:any = [];
  farmacias:any = [];
  flag = 0;

  buscador: FormGroup = this.formBuilder.group({
    producto: ""
  });

  miFormulario:FormGroup = this.formBuilder.group({
    nombre: ""
  });

  ngOnInit(): void {

  }

  mostrarProductoMasBarato() {
    const formValue = this.buscador.value;
    console.log(formValue);

    this.servicio.mostrarProductosMasBaratos(formValue.producto).subscribe((res) => {
      if (res.length != 0) {
        this.productos = res;
        console.log(this.productos);
        this.flag = 1;
      }
      else {
        this.router.navigate(['**']);
        //this.flag = 2;
      }
    });

    this.servicio.mostrarFarmacias().subscribe((res) => {
      this.farmacias = res;
      console.log(this.farmacias);
    }); 
  }
  
  opcionesFarmacias: any[] = [
    { name: 'SIMI', value: 'SIMI', checked: true },
    { name: 'ECO', value: 'ECO', checked: true },
    { name: 'REDFARMA', value: 'REDFARMA', checked: true},
    { name: 'SALCO', value: 'SALCO', checked: true},
    { name: 'AHUMADA', value: 'AHUMADA', checked: true}
  ];

  farmaciasSeleccionadas: string[] = ['SIMI', 'ECO', 'REDFARMA', 'SALCO', 'AHUMADA'];

  constructor(private servicio:AppService, private formBuilder: FormBuilder, private router: Router) {
    this.miFormulario = this.formBuilder.group({});
  }

  mostrarTabla: number[] = [1,2,3,4,5];

  filtrarFarmacias() {
    console.log(this.farmaciasSeleccionadas);
    this.mostrarTabla = [];
    this.opcionesFarmacias
  
    if (this.farmaciasSeleccionadas.includes('SIMI')) {
      this.mostrarTabla.push(1);
    }

    if (this.farmaciasSeleccionadas.includes('ECO')) {
      this.mostrarTabla.push(2);
    }

    if (this.farmaciasSeleccionadas.includes('REDFARMA')) {
      this.mostrarTabla.push(3);
    }

    if (this.farmaciasSeleccionadas.includes('SALCO')) {
      this.mostrarTabla.push(4);
    }

    if (this.farmaciasSeleccionadas.includes('AHUMADA')) {
      this.mostrarTabla.push(5);
    }
  
    console.log(this.mostrarTabla);
  }

  guardarIdFarmacias(event: any, value: string) {
    const isChecked = event.target.checked;
    if (isChecked) {
      this.farmaciasSeleccionadas.push(value);
    } else {
      const index = this.farmaciasSeleccionadas.indexOf(value);
      if (index !== -1) {
        this.farmaciasSeleccionadas.splice(index, 1);
      }
    }
  }
}

