#!/bin/bash
# Definieer het bestand waar de versie in aangepast moet worden
applicatie="mios-agent"
pad_applicatie="./mios-agent"
pad_rpmspec="../rpmbuild/SPECS/$applicatie.spec"

function gebruik {
	echo -e "\nDit script kan gebruikt worden om de versie van de $applicatie te verhogen"
	echo "Gebruik:"
	echo -e "\t$0 {opties}"
	echo -e "\nOpties:"
	echo -e "\t-h\t- Huidige versie opvragen"
	echo -e "\t-n\t- Nieuwe versie opgeven (moet 0.0 zijn)"
	echo -e "\nVoorbeeld:"
	echo -e "\t$0 -n 3.3"
	echo -e "\nDit zet de huidige versie van de $applicatie op 3.3\n"
	exit 1
}

function get_regelnummer {
	local __pad=$1
	local __zoekstring=$2
	local __regelnummer=$3
	if [[ "$__regelnummer" ]]; then
		eval $__regelnummer=`grep -n "$__zoekstring" $__pad | awk -F":" '{print $1}'`
	else
		echo "Te weinig parameters meegegeven aan functie $FUNCNAME"
		exit 1
	fi
}

function get_huidige_versie {
	local __regelnummer=$1
	local __pad=$2
	local __versienummer=$3
	if [[ "$__versienummer" ]]; then
		eval $__versienummer=`awk 'NR=='$__regelnummer'' $__pad | awk -F'"' '{print $2}'`
	else
		echo "Te weinig parameters meegegeven aan functie $FUNCNAME"
		exit 1
	fi
}

function get_rpmspec_huidige_versie {
	local __regelnummer=$1
	local __pad=$2
	local __versienummer=$3
	if [[ "$__versienummer" ]]; then
		eval $__versienummer=`awk 'NR=='$__regelnummer'' $__pad | awk '{print $2}'`
	else
		echo "Te weinig parameters meegegeven aan functie $FUNCNAME"
		exit 1
	fi
}

function set_nieuwe_versie {
	local __regelnummer=$1
	local __pad=$2
	local __zoekstring=$3
	local __nieuwe_versie=$4
	if [[ "$__nieuwe_versie" ]]; then
		#check of versienummer wel goed is. Moet n.n zijn
		re='^[0-9]*\.[0-9]*$'
		if ! [[ $__nieuwe_versie =~ $re ]]; then
			echo -e "\nOngeldige versie opgegeven: $__nieuwe_versie"
			echo -e "Versie moet als n.n opgegeven worden. Bijvoorbeeld 4.0\n"
			exit 1
		else
			# check decimal
			decimal=`echo $__nieuwe_versie | awk -F'.' '{print $2}'`
			if [ "$decimal" = "" ]; then
				echo -e "\nOngeldige versie opgegeven: $__nieuwe_versie"
				echo -e "Versie moet als n.n opgegeven worden. Bijvoorbeeld 4.0\n"
				exit 1
			else
				# Verwijder oude versie
				sed -i -e $__regelnummer'd;' $__pad
				# Zet nieuwe versie
#				sed -i $__regelnummer'i__version__   = "'$__nieuwe_versie'"' $__pad
				if [[ $__pad == *"rpm"* ]]; then
					sed -i $__regelnummer'iVersion:        '$__nieuwe_versie $__pad
				else
					sed -i $__regelnummer'i__version__   = "'$__nieuwe_versie'"' $__pad
				fi
			fi
		fi
	else
		echo "Te weinig parameters meegegeven aan functie $FUNCNAME"
		exit 1
	fi
	echo -e "\nNieuwe versie van $__pad is: $__nieuwe_versie\n"
}

if [ ! "$1" ]; then
	gebruik
fi

while getopts ":hn:" opt; do
	case $opt in
		h)
			get_regelnummer $pad_applicatie "__version__" regelnummer
			get_huidige_versie $regelnummer $pad_applicatie huidige_versie
			get_regelnummer $pad_rpmspec "Version" regelnummer
			get_rpmspec_huidige_versie $regelnummer $pad_rpmspec huidige_rpmspec_versie
			echo -e "\nHuidige versie van $pad_applicatie is: $huidige_versie"
			echo -e "\nHuidige versie van $pad_rpmspec is: $huidige_rpmspec_versie\n"
			if [ "$huidige_versie" != "$huidige_rpmspec_versie" ]; then
				echo -e "\n\e[7m\e[1mLET OP!"
				printf '%-100s\n' "        De versies van $pad_applicatie en $pad_rpmspec zijn niet gelijk."
				printf '%-100s\n' "        Mogelijk is 1 van de bestanden met de hand bijgewerkt waardoor het niet meer klopt."
				printf '%-100s\n' "        Let dus op met het opnieuw toekennen van een versie!"
				printf '%-100s\n' "        Zoek goed uit wat nu de juiste versie is en pruts niet meer handmatig in de bestanden!"
				echo -e "\e[0m"
			fi
			;;
		n)
			# Zet versie van mios-agent
			get_regelnummer $pad_applicatie "__version__" regelnummer
			set_nieuwe_versie $regelnummer $pad_applicatie "__version__" $OPTARG
			# Zet versie van RPMBUILD SPEC
			get_regelnummer $pad_rpmspec "Version" regelnummer
			set_nieuwe_versie $regelnummer $pad_rpmspec "Version" $OPTARG
			;;
		:)
			echo "Optie $OPTARG heeft een argument nodig."
			;;
		*|?)
			echo "Ongeldige optie: -$OPTARG"
			;;
	esac
done
